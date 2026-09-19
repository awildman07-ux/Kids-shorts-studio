const scenes=[
{name:"Strange Tracks",cap:"Whoa! WHO made these tracks?!",fact:"Look at the whole trail before guessing who made it.",voice:"Whoa, Maya! Look at these tracks! They’re fresh, and they lead right into the woods!",speaker:"Benji"},
{name:"Follow the Trail",cap:"Detective mode: ON!",fact:"Wild animals use trails to find food, water, shelter, and safe routes.",voice:"Detective mode on! Let’s follow from a safe distance and stay together while we look for clues!",speaker:"Benji"},
{name:"The Mystery Clue",cap:"Big prints... little mystery!",fact:"Tracks can show direction, speed, and sometimes how an animal moved.",voice:"Check out the toes and the spaces between prints. Tracks can tell us which way an animal traveled!",speaker:"Benji"},
{name:"Poof! Gone!",cap:"The tracks disappeared!",fact:"Soft mud and leaves can hide tracks surprisingly fast.",voice:"Poof! The trail vanished. Mud, leaves, and changing ground can hide tracks. Nature is sneaky!",speaker:"Benji"},
{name:"RUSTLE!",cap:"RUSTLE! Look over there!",fact:"Raccoons are mostly active at night and are great climbers.",voice:"RUSTLE! Whoa! Look over there! It’s a raccoon. Mystery solved, detective team!",speaker:"Benji"},
{name:"Adventure Continues",cap:"Every trail tells a story!",fact:"Best wildlife rule: watch quietly, give animals space, and leave no trace.",voice:"We solved it! Remember: watch quietly, give wildlife space, and leave nature just as you found it!",speaker:"Benji"}
];
let i=0,playing=false,elapsed=0,timerId,voices=[];
const $=s=>document.querySelector(s);
function cards(){$("#cards").innerHTML=scenes.map((s,n)=>'<button class="card" data-n="'+n+'"><b>'+String(n+1).padStart(2,"0")+'</b><span>'+s.name+'</span></button>').join("");document.querySelectorAll(".card").forEach((b,n)=>b.onclick=()=>go(n))}
function faceScene(){const sc=$("#scene");sc.classList.remove("scenePop");void sc.offsetWidth;sc.classList.add("scenePop")}
function render(){
 const s=scenes[i];
 $("#sceneName").textContent="Scene "+(i+1)+" — "+s.name;
 $("#caption").textContent=s.cap;
 $("#voice").textContent=s.voice;
 $("#fact b").textContent=s.fact;
 document.querySelectorAll(".card").forEach((b,n)=>b.classList.toggle("active",n===i));
 $("#timer").textContent="0:"+String(Math.min(59,elapsed)).padStart(2,"0")+" / 1:00";
 $("#titleCard").style.display=i===0&&elapsed<4?"block":"none";
 $("#maya").style.display="block";
 $("#raccoon").style.display=i>=4?"block":"none";
 $("#fact").classList.remove("factPop");void $("#fact").offsetWidth;$("#fact").classList.add("factPop");
 const trackCount=i===3?4:8;
 $("#tracks").innerHTML=i<4?Array.from({length:trackCount},(_,n)=>'<span class="track" style="left:'+((n*13+7)%88)+'%;bottom:'+(n*12+5)+'%;animation-delay:'+n*.07+'s"></span>').join(""):"";
 $("#benji").style.left=[9,22,31,41,51,60][i]+"%";
 $("#maya").style.right=[8,15,23,27,19,12][i]+"%";
 $("#maya").style.transform=i===2?"scale(1.04) rotate(-2deg)":i===4?"scale(1.08) rotate(3deg)":"";
 $("#benji").style.transform=i===0?"rotate(-3deg)":i===4?"rotate(4deg)":"";
 $("#scene").dataset.scene=i;
 faceScene();
 if(i===4)burst();
}
function burst(){const sc=$("#scene");for(let n=0;n<18;n++){const e=document.createElement("span");e.className="spark";e.textContent=["✦","•","★","✧"][n%4];e.style.left=(35+Math.random()*34)+"%";e.style.bottom=(28+Math.random()*35)+"%";e.style.animationDelay=(Math.random()*.3)+"s";sc.appendChild(e);setTimeout(()=>e.remove(),1800)}}
function clap(){if(!("AudioContext"in window)&&!("webkitAudioContext"in window))return;const C=window.AudioContext||window.webkitAudioContext,c=new C();[0,.09,.18].forEach((d,n)=>{const o=c.createOscillator(),g=c.createGain();o.frequency.value=[520,660,820][n];g.gain.setValueAtTime(.0001,c.currentTime+d);g.gain.exponentialRampToValueAtTime(.06,c.currentTime+d+.01);g.gain.exponentialRampToValueAtTime(.0001,c.currentTime+d+.11);o.connect(g);g.connect(c.destination);o.start(c.currentTime+d);o.stop(c.currentTime+d+.12)});setTimeout(()=>c.close(),500)}
function chooseVoice(){voices=speechSynthesis.getVoices();return voices.find(v=>/en-US/i.test(v.lang)&&/Samantha|Google US English|Jenny|Zira|Ava/i.test(v.name))||voices.find(v=>/en-US/i.test(v.lang))||voices.find(v=>/^en/i.test(v.lang))}
function speak(){if(!("speechSynthesis"in window))return;speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(scenes[i].voice);const v=chooseVoice();if(v)u.voice=v;u.rate=.98;u.pitch=1.22;u.volume=1;speechSynthesis.speak(u);if(i===4)clap()}
if("speechSynthesis"in window)speechSynthesis.onvoiceschanged=()=>{voices=speechSynthesis.getVoices()};
function go(n){i=(n+6)%6;elapsed=i*10;render();if(playing)speak()}
function play(){playing=!playing;$("#playTop").textContent=playing?"❚❚ Pause":"▶ Play Episode";if(playing){if(elapsed>=60){elapsed=0;i=0}render();speak();clearInterval(timerId);timerId=setInterval(()=>{elapsed++;const ni=Math.min(5,Math.floor(elapsed/10));if(ni!==i){i=ni;render();speak()}else render();if(elapsed>=60){clearInterval(timerId);playing=false;$("#playTop").textContent="▶ Replay Episode";speechSynthesis.cancel()}},1000)}else{clearInterval(timerId);speechSynthesis.cancel()}}
$("#playTop").onclick=play;$("#prev").onclick=()=>go(i-1);$("#next").onclick=()=>go(i+1);cards();render();