"""Production controller deadline and editor semantics with TEST ONLY services.

No signed peer/GUI acceptance is claimed here. The production client and editor
are compiled; only endpoint discovery and host replies are fixture boundaries.
"""
import json
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import uuid
import pytest

ROOT=Path(__file__).resolve().parents[1]
pytestmark=pytest.mark.skipif(sys.platform!='darwin',reason='AppKit client')

@pytest.fixture(scope='module')
def control_client(tmp_path_factory):
    folder=tmp_path_factory.mktemp('nyra-control-client')
    source=r'''
import AppKit
import Darwin
struct BridgeSelection { let endpoint:String }
struct Endpoint {let producer_instance_id:String;let control_protocol:String?;let control_socket:String?;var focus_protocol:String?=nil;var focus_socket:String?=nil}
final class FixturePeer {
 var isTerminated=false
 static var fixtureActivations=0
 func activate(options:NSApplication.ActivationOptions)->Bool {Self.fixtureActivations+=1;return true}
}
final class NyraStatusClient {
 static var delay:Double=0
 static var dedicatedFocus=false
 static func readEndpoint(_ path:String)throws->Endpoint {
   Thread.sleep(forTimeInterval:delay)
   return Endpoint(producer_instance_id:path,control_protocol:dedicatedFocus ? nil:"twos.nyra.control.v1",control_socket:dedicatedFocus ? nil:"/private/tmp/twos-nyra-status-"+path+"/control.sock",focus_protocol:dedicatedFocus ? "twos.nyra.focus.v1":nil,focus_socket:dedicatedFocus ? "/private/tmp/twos-nyra-status-"+path+"/focus.sock":nil)
 }
 static func securePath(_ path:String,mode:mode_t,socket:Bool)throws{}
 static func verifyPeer(_ fd:Int32,selection:BridgeSelection)throws->FixturePeer {FixturePeer()}
}
let ink=NSColor.black
class TaskLabelButton:NSButton{}
'''
    source+=(ROOT/'Sources/NyraControlClient.swift').read_text()
    source+=(ROOT/'Sources/DraftRecovery.swift').read_text()
    source+=(ROOT/'Sources/TaskControls.swift').read_text().split('extension Companion {',1)[0]
    source+=r'''
extension CompanionDraftRecovery {
 static func delayTestLoad(){io.async{Thread.sleep(forTimeInterval:0.25)}}
}
let mode=CommandLine.arguments[1],host=CommandLine.arguments[2]
let client=NyraControlClient()
var replies=[[String:Any]]()
func spin(_ duration:Double){RunLoop.main.run(until:Date(timeIntervalSinceNow:duration))}
func awaitFixture(_ condition:()->Bool){
 let end=Date(timeIntervalSinceNow:2)
 while !condition() && Date()<end {spin(0.01)}
 precondition(condition(),"bounded asynchronous fixture completion not received")
}
if mode=="focusDedicated" || mode=="focusLegacy" {
 NyraStatusClient.dedicatedFocus=mode=="focusDedicated"
 client.request("focusHost",selection:BridgeSelection(endpoint:host)){replies.append($0)}
 spin(0.3)
 precondition(replies.count==1 && replies[0]["state"] as? String=="TEST_ONLY" && FixturePeer.fixtureActivations==1)
 precondition(client.activeMethods.isEmpty)
} else if mode=="deadline" {
 NyraStatusClient.delay=4.3
 client.request("submit",selection:BridgeSelection(endpoint:host)){replies.append($0)}
 spin(4.7)
 precondition(replies.count==1 && replies[0]["error"] as? String=="CONTROL_DEADLINE_STATUS_UNKNOWN_NO_RETRY")
 precondition(client.activeMethods.isEmpty)
} else if mode=="reset" {
 NyraStatusClient.delay=0.25
 client.inspect(selection:BridgeSelection(endpoint:host)){}
 DispatchQueue.main.asyncAfter(deadline:.now()+0.04){client.reset();client.error="NEW_CONNECTION_STATE"}
 spin(0.6)
 precondition(client.error=="NEW_CONNECTION_STATE" && client.tasks.isEmpty && !client.inspecting)
} else if mode=="normal" {
 client.request("inspect",selection:BridgeSelection(endpoint:host)){replies.append($0)}
 spin(0.2)
 precondition(replies.count==1 && replies[0]["state"] as? String=="TEST_ONLY")
 } else if mode=="recovery" {
 let app=NSApplication.shared;app.setActivationPolicy(.accessory)
 let root=URL(fileURLWithPath:"/private/tmp/twos-nyra-status-"+host).appendingPathComponent("recovery")
 try! FileManager.default.createDirectory(at:root,withIntermediateDirectories:false,attributes:[.posixPermissions:0o700])
 let store=CompanionDraftRecovery(root:root)
 let task:[String:Any]=["target":String(repeating:"a",count:64),"provider":"TEST ONLY","title":"recovery fixture","canSteer":true]
 let first=CompanionDraftRecovery.Record(id:UUID().uuidString,target:task["target"] as! String,title:"original test",provider:"TEST ONLY",text:"中文未确认输入",uncertain:true,createdAt:0)
 var saved=false;store.save(first){saved=$0};awaitFixture{saved}
 let attributes=try! FileManager.default.attributesOfItem(atPath:store.file.path)
 precondition((attributes[.posixPermissions] as! NSNumber).intValue==0o600)
 let newer=CompanionDraftRecovery.Record(id:UUID().uuidString,target:first.target,title:first.title,provider:first.provider,text:"newer text",uncertain:true,createdAt:1)
 let nextEditorStore=CompanionDraftRecovery(root:root)
 nextEditorStore.save(newer){saved=$0};store.clear(id:first.id);spin(0.15)
 var loaded:CompanionDraftRecovery.Record?;store.load{loaded=try! $0.get()};awaitFixture{loaded != nil}
 precondition(loaded?.id==newer.id,"a late acknowledgement must not erase newer input")
 let editor=CompanionTaskEditor(task:task,zh:true);editor.recovery=store
 var requests=0;editor.request={_,_,_ in requests+=1}
 CompanionDraftRecovery.delayTestLoad()
 editor.load();editor.submit();editor.saveDraft()
 precondition(editor.loading && requests==0 && !editor.send.isEnabled,"pending recovery cannot send or overwrite a draft")
 awaitFixture{!editor.loading};editor.submit();editor.saveDraft()
 precondition(editor.restoredRecovery && editor.text.string=="newer text" && !editor.text.isEditable && !editor.send.isEnabled && requests==0,"reopening recovery must never resume/redirect/send or overwrite a host draft; restored=\(editor.restoredRecovery), loading=\(editor.loading), textMatch=\(editor.text.string=="newer text"), editable=\(editor.text.isEditable), send=\(editor.send.isEnabled), requests=\(requests)")
 editor.cancel();loaded=nil;store.load{loaded=try! $0.get()};awaitFixture{loaded != nil};precondition(loaded?.id==newer.id)
 var cleared=false;store.clear(id:newer.id){cleared=$0};awaitFixture{cleared}
 // A malicious/unexpected symlink cannot be read as user draft data.
 try! FileManager.default.createSymbolicLink(at:store.file,withDestinationURL:root.appendingPathComponent("absent"))
 var rejected=false;store.load{if case .failure = $0{rejected=true}};awaitFixture{rejected}
 try! FileManager.default.removeItem(at:store.file)
 // A live failed mutation exposes recovery immediately, without requiring a
 // restart or silently resubmitting when the connection returns.
 let rejectedEditor=CompanionTaskEditor(task:task,zh:false);rejectedEditor.recovery=store
 rejectedEditor.revision="test-live";rejectedEditor.text.string="uncertain live input";rejectedEditor.dirty=true
 rejectedEditor.request={_,_,reply in requests+=1;reply(["error":"HOST_CONNECTION_STATE_UNCONFIRMED_DRAFT_RETAINED"])}
 rejectedEditor.submit();awaitFixture{rejectedEditor.restoredRecovery}
 precondition(requests==1 && rejectedEditor.restoredRecovery && !rejectedEditor.useSaved.isHidden && !rejectedEditor.send.isEnabled)
 rejectedEditor.submit();rejectedEditor.cancel();spin(0.1);precondition(requests==1)
 loaded=nil;store.load{loaded=try! $0.get()};awaitFixture{loaded != nil};precondition(loaded?.text=="uncertain live input")
 requests=0
 let fail=CompanionTaskEditor(task:task,zh:false);fail.recovery=CompanionDraftRecovery(root:root.appendingPathComponent("missing"));fail.revision="test";fail.text.string="do not send without recovery";fail.dirty=true
 fail.request={_,_,_ in requests+=1};fail.submit();awaitFixture{!fail.busy}
 precondition(requests==0 && !fail.busy && fail.dirty && fail.revision.isEmpty)
 fail.panel.orderOut(nil)
 } else if mode=="stop" {
 let app=NSApplication.shared;app.setActivationPolicy(.accessory)
 let target=String(repeating:"a",count:64),other=String(repeating:"b",count:64)
 let task:[String:Any]=["target":target,"side":"right","provider":"Codex","title":"TEST ONLY stop feedback","state":"running","fresh":true,"canStop":true]
 let card=CompanionTaskCard();var calls=0,actionID=""
 card.onStop={row,id in calls+=1;actionID=id;precondition(row["target"] as? String==target)}
 card.update([task],fresh:true,authorized:true,zh:false)
 card.stopTask();card.stopTask()
 precondition(calls==1 && !card.stop.isEnabled && card.subtitle.title.contains("Stopping"))
 // Normal snapshots must not re-enable duplicate Stop or erase its feedback.
 card.update([task],fresh:true,authorized:true,zh:false);card.stopTask()
 precondition(calls==1 && !card.stop.isEnabled && card.subtitle.title.contains("Stopping"))
 card.finishStop(actionID,target:target,result:["error":"CONTROL_DEADLINE_STATUS_UNKNOWN_NO_RETRY"])
 card.update([task],fresh:true,authorized:true,zh:true)
 precondition(card.title.title=="TEST ONLY stop feedback" && card.subtitle.title.contains("停止未确认") && card.subtitle.toolTip!.contains("不要重复发送") && !card.stop.isEnabled)
 precondition(card.stopObservation["error"] as? String=="CONTROL_DEADLINE_STATUS_UNKNOWN_NO_RETRY")
 card.update([task.merging(["state":"cancelled","canStop":false]){_,n in n}],fresh:true,authorized:true,zh:true)
 precondition(card.subtitle.title.contains("已停止") && !card.stop.isEnabled && card.stop.toolTip!.contains("执行已结束"))
 card.stopTask();precondition(calls==1)
 // Switching tasks isolates both feedback and late callback; no redirect.
 let otherTask=task.merging(["target":other,"title":"TEST ONLY other task"]){_,n in n}
 card.update([otherTask],fresh:true,authorized:true,zh:false)
 card.finishStop(actionID,target:target,result:["state":"stopping"])
 precondition(card.subtitle.title.contains("Running") && card.stop.isEnabled && card.title.title=="TEST ONLY other task")
 card.update([otherTask],fresh:false,authorized:true,zh:false);card.stopTask()
 precondition(calls==1 && card.subtitle.title.contains("awaiting update"))
 // Acceptance is not completion. A bounded wait exposes unknown, never success.
 card.update([task],fresh:true,authorized:true,zh:false)
 card.stopAttempt=nil;card.render();card.stopTask()
 card.finishStop(actionID,target:target,result:["state":"stopping"])
 let old=card.stopAttempt!
 card.stopAttempt=CompanionTaskCard.StopAttempt(id:old.id,target:old.target,started:old.started-13,at:old.at,response:old.response,error:nil,finished:old.finished)
 card.render();precondition(card.subtitle.title.contains("Stop unconfirmed") && !card.stop.isEnabled)
 card.update([task.merging(["state":"completed_unverified","canStop":false]){_,n in n}],fresh:true,authorized:true,zh:false)
 precondition(card.subtitle.title.contains("unverified") && !card.subtitle.title.contains("Stopped"))
 card.panel.orderOut(nil)
} else if mode=="editor" {
 let app=NSApplication.shared;app.setActivationPolicy(.accessory)
 let task:[String:Any]=["target":String(repeating:"a",count:64),"provider":"TEST ONLY","title":"isolated editor","canSteer":true]
 let editor=CompanionTaskEditor(task:task,zh:true)
 precondition(editor.panel.canBecomeKey && !CompanionTaskPanel().canBecomeKey)
 var methods=[String](),values=[[String:Any]]()
 editor.request={method,payload,reply in
   methods.append(method);values.append(payload)
   if method=="draft" && payload["text"]==nil {reply(["text":"原草稿","revision":"original","queue":[["id":"q1","label":"pending"]]])}
   else{reply(["state":"saved","revision":"new"])}
 }
 editor.load();precondition(editor.text.string=="原草稿" && editor.revision=="original")
 editor.text.string="中文补充";editor.dirty=true;editor.mode.selectItem(at:1);editor.submit()
 precondition(methods.last=="submit" && values.last?["target"] as? String==task["target"] as? String && values.last?["mode"] as? String=="steer")
 // An active IME composition is never sent as a partial instruction.
 let previous=methods.count
 editor.text.setMarkedText("拼音候选",selectedRange:NSRange(location:0,length:4),replacementRange:NSRange(location:NSNotFound,length:0))
 precondition(editor.text.hasMarkedText());editor.submit();precondition(methods.count==previous)
 editor.text.unmarkText();editor.text.string="保留取消草稿";editor.dirty=true;editor.cancel()
 precondition(methods.last=="draft" && values.last?["text"] as? String=="保留取消草稿")
 precondition(values.allSatisfy{$0["target"] as? String==task["target"] as? String})
 // Positive edit of a still-pending item uses editQueue, never submit.
 let queued=CompanionTaskEditor(task:task,zh:false)
 var queuedMethods=[String](),editedText="",editedID=""
 queued.request={method,payload,reply in
   queuedMethods.append(method)
   if method=="editQueue" {editedText=payload["text"] as? String ?? "";editedID=payload["queueID"] as? String ?? "";reply(["state":"edited","revision":"q-after"])}
   else {reply(["text":payload["queueID"]==nil ? "":"original queued instruction","revision":"q-before","queue":[["id":"pending-exact","label":"TEST ONLY"]],"canSubmit":true])}
 }
 queued.load();queued.pending.selectItem(at:1);queued.selectQueued()
 precondition(queued.queueID=="pending-exact" && queued.text.string=="original queued instruction")
 precondition(queued.mode.indexOfSelectedItem==0 && queued.status.stringValue.contains("Enter saves") && !queued.status.stringValue.contains("Autosaved"))
 queued.text.string="edited unsent instruction";queued.dirty=true;queued.submit()
 precondition(editedID=="pending-exact" && editedText=="edited unsent instruction" && !queuedMethods.contains("submit"))
 queued.panel.orderOut(nil)
 precondition(CompanionTaskCard.state("failed",zh:true)=="失败" && CompanionTaskCard.state("idle",zh:true).contains("待核验"))
 let card=CompanionTaskCard()
 card.update([task.merging(["side":"left","fresh":true,"state":"running","canAppend":true,"canStop":true]){_,new in new}],fresh:true,authorized:true,zh:false)
 precondition(card.panel.frame.height==64 && card.append.isHidden && card.stop.isHidden && card.picker.isHidden)
 precondition(card.append.image != nil && card.append.title.isEmpty && card.expand.isHidden)
 card.hovered=true;card.layout();precondition(!card.append.isHidden && !card.stop.isHidden)
 var directTarget="";card.onAppend={directTarget=$0["target"] as? String ?? ""};card.edit()
 precondition(directTarget==task["target"] as? String && !card.expanded,"one click must open the exact task without expansion")
 precondition(card.title.cell?.wraps==false && card.title.cell?.lineBreakMode == .byTruncatingTail && card.subtitle.title.contains("Left"))
 card.toggleExpanded();precondition(card.panel.frame.height==64 && !card.append.isHidden && !card.stop.isHidden && card.append.isEnabled)
 card.update([task.merging(["side":"left","fresh":false,"state":"activity_unknown"]){_,new in new}],fresh:false,authorized:true,zh:true)
 precondition(!card.append.isEnabled && card.subtitle.title.contains("待更新") && card.expanded)
 card.toggleExpanded();precondition(card.panel.frame.height==64 && card.title.title=="isolated editor")
 precondition(card.expand.acceptsFirstMouse(for:nil) && card.append.acceptsFirstMouse(for:nil) && !card.append.needsPanelToBecomeKey)
 precondition(!card.panel.hidesOnDeactivate && card.panel.level.rawValue>NSWindow.Level.floating.rawValue)
 let left=task.merging(["side":"left","scope":"left-chat","fresh":true,"state":"running","canEdit":true,"canAppend":true]){_,new in new}
 let right=task.merging(["target":String(repeating:"b",count:64),"scope":"right-chat","side":"right","fresh":true,"state":"running","canEdit":true]){_,new in new}
 card.update([left,right],fresh:true,authorized:true,zh:false)
 precondition(card.title.title.hasPrefix("L · Running") && card.subtitle.title.hasPrefix("R · Running"),"state must precede long titles on both rows")
 var focusTarget="";card.onFocus={focusTarget=$0};card.focusSecond()
 precondition(focusTarget==right["target"] as? String,"second displayed row must focus its own task")
 var unavailable=false;card.onFocusUnavailable={unavailable=true}
 card.focusRow(["side":"left","title":"readonly snapshot"])
 precondition(unavailable && focusTarget==right["target"] as? String,"read-only card cannot silently redirect to another target")
 card.selected=left["target"] as? String
 let next=left.merging(["target":String(repeating:"c",count:64)]){_,new in new}
 card.update([right,next],fresh:true,authorized:true,zh:false)
 precondition(card.task?["side"] as? String=="left","turn refresh must preserve the selected conversation, not move to the other side")
 let ended=next.merging(["state":"completed_unverified","canAppend":false,"canStop":false]){_,new in new}
 card.update([ended],fresh:true,authorized:true,zh:false);card.toggleExpanded()
 precondition(card.append.isEnabled && !card.stop.isEnabled,"ended owned task keeps draft editing available")
 var clickedTarget="";card.onAppend={clickedTarget=$0["target"] as? String ?? ""};card.edit()
 precondition(clickedTarget==ended["target"] as? String)
 // A completed task may open an editor and save; it cannot accidentally start a new turn.
 let endedEditor=CompanionTaskEditor(task:ended,zh:true)
 precondition(endedEditor.panel.frame.size==NSSize(width:360,height:190))
 precondition(endedEditor.textView(endedEditor.text,doCommandBy:#selector(NSResponder.insertNewline(_:))),"Enter is handled by the actual composer delegate")
 var endedMethods=[String]()
 endedEditor.request={method,_,reply in endedMethods.append(method);reply(["text":"","revision":"ended","canSubmit":false,"state":"saved"])}
 endedEditor.load();endedEditor.text.string="后续草稿";endedEditor.dirty=true;endedEditor.saveDraft();endedEditor.submit()
 precondition(endedMethods==["draft","draft"] && !endedEditor.send.isEnabled && endedEditor.text.isEditable)
 endedEditor.panel.orderOut(nil)
 // Explicit Send during an autosave waits for that save; two clicks produce
 // one submission and a read-only receipt check, never an implicit resubmit.
 let continuous=CompanionTaskEditor(task:task,zh:false)
 var continuousMethods=[String](),saveReply:(([String:Any])->Void)?,sent=false
 continuous.request={method,payload,reply in
   continuousMethods.append(method)
   if method=="draft",payload["text"] != nil {saveReply=reply}
   else if method=="submit" {sent=true;reply(["state":"sending","receipt":"test-receipt"])}
   else if payload["receipt"] != nil {reply(["receiptState":"accepted"])}
   else {reply(["text":"","revision":sent ? "after":"before","queue":[],"canSubmit":true])}
 }
 continuous.load();continuous.text.string="exact explicit supplement";continuous.dirty=true;continuous.saveDraft()
 continuous.submit();continuous.submit()
 precondition(continuousMethods==["draft","draft"] && continuous.pendingSubmit != nil)
 saveReply?(["state":"saved","revision":"saved"])
 precondition(continuousMethods==["draft","draft","submit","draft","draft"] && continuous.text.string.isEmpty && continuous.revision=="after" && !continuous.dirty && continuous.text.isEditable)
 continuous.panel.orderOut(nil)
 // Closing while autosave is pending retains the frozen target only until
 // the save is confirmed; a later pencil click must not reopen an old task.
 let closing=CompanionTaskEditor(task:task,zh:false)
 var closedAfterSave=false,closeSaveReply:(([String:Any])->Void)?
 closing.closed={closedAfterSave = !$0.busy && !$0.dirty}
 closing.request={method,payload,reply in
   if payload["text"] != nil {closeSaveReply=reply}
   else {reply(["text":"","revision":"close-before","queue":[],"canSubmit":true])}
 }
 closing.load();closing.text.string="retained close draft";closing.dirty=true;closing.saveDraft();closing.cancel()
 precondition(!closedAfterSave && closing.dismissed && closing.busy)
 closeSaveReply?(["state":"saved","revision":"close-after"])
 precondition(closedAfterSave && !closing.dirty && closing.text.string=="retained close draft")
 let uncertainClose=CompanionTaskEditor(task:task,zh:false)
 var receiptReply:(([String:Any])->Void)?,releasedUnconfirmed=false
 uncertainClose.closed={releasedUnconfirmed = !$0.dirty && !$0.busy}
 uncertainClose.request={method,payload,reply in
   if method=="submit" {reply(["state":"sending","receipt":"pending-test-receipt"])}
   else if payload["receipt"] != nil {receiptReply=reply}
   else {reply(["text":"","revision":"uncertain-before","queue":[],"canSubmit":true])}
 }
 uncertainClose.load();uncertainClose.text.string="unconfirmed supplement";uncertainClose.dirty=true;uncertainClose.submit();uncertainClose.cancel()
 precondition(!releasedUnconfirmed && uncertainClose.dirty && uncertainClose.revision.isEmpty)
 receiptReply?(["receiptState":"accepted"])
 precondition(uncertainClose.text.string=="unconfirmed supplement" && uncertainClose.dirty,"late reply after close cannot discard unconfirmed input or send again")
 precondition(CompanionControlText.error("TASK_CHANGED_DRAFT_RETAINED",zh:true).contains("没有改发"))
 var finish:(([String:Any])->Void)?
 editor.request={_,_,reply in finish=reply}
 editor.revision="pending-send";editor.submit()
 precondition(editor.busy && !editor.text.isEditable && !editor.send.isEnabled)
 finish?(["error":"CONTROL_DEADLINE_STATUS_UNKNOWN_NO_RETRY"])
 precondition(!editor.busy && editor.text.isEditable && !editor.send.isEnabled && editor.revision.isEmpty && editor.dirty && editor.status.stringValue.contains("不要重复发送"))
 let retained=editor.text.string;editor.submit();precondition(!editor.busy && editor.text.string==retained)
 editor.panel.orderOut(nil)
}
print("TEST_ONLY_PASS "+mode)
'''
    swift=folder/'main.swift';swift.write_text(source);binary=folder/'client'
    compiled=subprocess.run(['xcrun','swiftc','-swift-version','5','-module-cache-path',str(folder/'cache'),'-framework','AppKit',str(swift),'-o',str(binary)],capture_output=True,text=True,timeout=90)
    assert compiled.returncode==0,compiled.stderr
    return binary

@pytest.mark.parametrize('mode',['deadline','reset','normal','recovery','editor','stop','focusDedicated','focusLegacy'])
def test_controller_deadline_reset_and_editor(control_client,mode):
    host=str(uuid.uuid4());root=Path('/private/tmp')/('twos-nyra-status-'+host);root.mkdir(mode=0o700)
    listener=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM);listener.bind(str(root/('focus.sock' if mode=='focusDedicated' else 'control.sock')));listener.listen();listener.settimeout(.05)
    captured=[];finished=threading.Event()
    def serve():
        while not finished.is_set():
            try:client,_=listener.accept()
            except socket.timeout:continue
            with client:
                client.settimeout(1);line=b''
                try:
                    while b'\n' not in line:
                        chunk=client.recv(8192)
                        if not chunk:break
                        line+=chunk
                    if line:
                        request=json.loads(line);captured.append(request)
                        client.sendall(json.dumps(dict(requestID=request['requestID'],hostInstance=host,state='TEST_ONLY')).encode()+b'\n')
                except (OSError,json.JSONDecodeError):pass
    worker=threading.Thread(target=serve);worker.start()
    try:
        result=subprocess.run([str(control_client),mode,host],capture_output=True,text=True,timeout=12)
        assert result.returncode==0,result.stdout+result.stderr
        assert 'TEST_ONLY_PASS '+mode in result.stdout
        assert len(captured)==(1 if mode in ('normal','focusDedicated','focusLegacy') else 0), 'Expired/reset client sent an operation after invalidation'
        if mode in ('focusDedicated','focusLegacy'):
            assert captured[0]['method']=='focus' and 'target' not in captured[0]
            assert captured[0]['protocol']==('twos.nyra.focus.v1' if mode=='focusDedicated' else 'twos.nyra.control.v1')
    finally:
        finished.set();worker.join(timeout=2);listener.close();shutil.rmtree(root)
