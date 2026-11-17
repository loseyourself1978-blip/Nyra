"""Deterministic presentation policy; not live-model or physical-click evidence."""
from pathlib import Path
import subprocess
import sys
import pytest

ROOT = Path(__file__).resolve().parents[1]
pytestmark = pytest.mark.skipif(sys.platform != "darwin", reason="Swift/CoreGraphics")

def test_readonly_activity_terminal_and_bounded_uncertainty(tmp_path):
    # Compile the actual event/reducer and presentation policy, not a Python copy.
    source = "import Foundation\nenum PreviewError: Error {case invalidManifest}\n"
    source += (ROOT / "Sources/ReactiveState.swift").read_text().split("struct R4Set:", 1)[0]
    source += (ROOT / "Sources/TaskPresentation.swift").read_text()
    source += r'''
func event(_ left:WorkState,_ right:WorkState = .idle,instance:String="host",session:String="chat",title:String="TEST ONLY left")->StatusEvent {
 var e=StatusEvent(schema_version:"twos.nyra.status.v4",producer_instance_id:instance,event_id:"event",sequence:1,timestamp:"2026-11-17T00:00:00Z",session_id:session,task_id:"task",state:left,source:"twos_runtime",simulation:false,evidence_ref:nil,activity_side:"both")
 e.pane_observations=[PaneObservation(side:"left",state:left,reason:"TEST_ONLY",fresh:true),PaneObservation(side:"right",state:right,reason:"TEST_ONLY",fresh:true)]
 e.task_labels=[]
 if [.running,.queued,.waiting_user].contains(left){e.task_labels!.append(TaskLabel(side:"left",provider:"ChatGPT",title:title))}
 if [.running,.queued,.waiting_user].contains(right){e.task_labels!.append(TaskLabel(side:"right",provider:"Claude",title:"TEST ONLY right"))}
 return e
}
var p=TaskPresentation()
func rows(_ e:StatusEvent,_ now:Double,_ connected:Bool=true,_ controls:[[String:Any]]=[],_ controlFresh:Bool=false)->[[String:Any]] {
 p.rows(event:e,connected:connected,lastReceipt:now,now:now,controls:controls,controlsFresh:controlFresh)
}
let left=event(.running)
precondition(TaskPresentation.controlsMatch(event:left,host:"host",session:"chat",task:"task"))
precondition(!TaskPresentation.controlsMatch(event:left,host:"old-host",session:"chat",task:"task"))
precondition(!TaskPresentation.controlsMatch(event:left,host:"host",session:"other-chat",task:"task"))
precondition(!TaskPresentation.controlsMatch(event:left,host:"host",session:"chat",task:"old-turn"))
precondition(!TaskPresentation.controlsMatch(event:left,host:"host",session:nil,task:nil),"older snapshots must not grant guessed action binding")
precondition(rows(left,10).count==1,"read-only activity must not require controls")
precondition(rows(event(.running,.waiting_user),11).count==2,"both sides must survive")
precondition(rows(event(.idle,.queued),12).count==1,"one terminal must not hide the other side")
precondition(rows(event(.cancelled),13).isEmpty,"confirmed terminal hides immediately")
precondition(rows(left,20).count==1)
let stale=rows(left,21,false)
precondition(stale.count==1 && stale[0]["state"] as? String=="activity_unknown" && stale[0]["target"]==nil)
precondition(rows(left,29,false).isEmpty,"stale heartbeats cannot prolong an old task indefinitely")
_ = rows(left,30)
precondition(rows(event(.activity_unknown,instance:"new-host"),31).isEmpty,"restart cannot replay old work")
_ = rows(left,40)
precondition(rows(event(.activity_unknown,session:"other-chat"),41).isEmpty,"new chat cannot inherit old title")
let target=String(repeating:"a",count:64)
let action:[String:Any]=["side":"left","provider":"ChatGPT","title":"TEST ONLY left","state":"running","fresh":true,"target":target,"canStop":true]
precondition(rows(left,50,true,[action],true)[0]["target"] as? String==target)
precondition(rows(left,51,true,[action],false)[0]["target"]==nil,"control outage cannot grant stale action")
let stopping=action.merging(["state":"stopping","canStop":false]){_,new in new}
let stoppingRow=rows(left,51.5,true,[stopping],true)[0]
precondition(stoppingRow["target"] as? String==target && stoppingRow["state"] as? String=="stopping","stopping keeps the same bound target until actual terminal")
precondition(rows(event(.running,title:"new task"),52,true,[action],true)[0]["target"]==nil,"old control card must not attach to new display")
precondition(rows(event(.completed_unverified),53).isEmpty,"unverified end is not ongoing activity")
print("PASS readonly/both/terminal/uncertainty/restart/session/control-binding")
'''
    swift = tmp_path / "main.swift"
    swift.write_text(source)
    binary = tmp_path / "policy-test"
    built = subprocess.run(["xcrun", "swiftc", "-swift-version", "5", "-module-cache-path", str(tmp_path / "cache"), str(swift), "-o", str(binary)], capture_output=True, text=True, timeout=90)
    assert built.returncode == 0, built.stderr
    result = subprocess.run([str(binary)], capture_output=True, text=True, timeout=5)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS readonly" in result.stdout
