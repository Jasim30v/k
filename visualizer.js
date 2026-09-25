let vizCanvas,vizCtx,vizAnimationId,contactData=[],vizPulse=0;
function initVisualizer(){vizCanvas=document.getElementById('vizCanvas');vizCtx=vizCanvas.getContext('2d');resizeViz();window.addEventListener('resize',resizeViz);for(let i=0;i<64;i++)contactData.push({val:0.1,sent:false});drawViz()}
function resizeViz(){const c=vizCanvas.parentElement;if(!c)return;vizCanvas.width=c.clientWidth;vizCanvas.height=c.clientHeight}
function drawViz(){vizAnimationId=requestAnimationFrame(drawViz);const w=vizCanvas.width,h=vizCanvas.height;vizCtx.fillStyle='rgba(5,5,16,0.25)';vizCtx.fillRect(0,0,w,h);const cx=w/2,cy=h/2,r=Math.min(w,h)*0.35;vizPulse+=0.05;
for(let i=0;i<contactData.length;i++){const d=contactData[i];const a=(i/contactData.length)*Math.PI*2+vizPulse*0.1;const rad=r+d.val*40;const x=cx+Math.cos(a)*rad;const y=cy+Math.sin(a)*rad;const col=d.sent?'0,255,204':'99,102,241';
vizCtx.beginPath();vizCtx.moveTo(cx,cy);vizCtx.lineTo(x,y);vizCtx.strokeStyle=`rgba(${col},${0.05+d.val*0.3})`;vizCtx.lineWidth=0.5+d.val*1.5;vizCtx.stroke();
vizCtx.beginPath();vizCtx.arc(x,y,1.5+d.val*6,0,Math.PI*2);vizCtx.fillStyle=`rgba(${col},${0.4+d.val*0.6})`;vizCtx.fill()}
const pulseR=8+Math.sin(vizPulse*2)*3;vizCtx.beginPath();vizCtx.arc(cx,cy,pulseR,0,Math.PI*2);const g=vizCtx.createRadialGradient(cx,cy,0,cx,cy,pulseR*3);g.addColorStop(0,'rgba(0,255,204,0.8)');g.addColorStop(1,'rgba(0,255,204,0)');vizCtx.fillStyle=g;vizCtx.fill();
vizCtx.beginPath();vizCtx.arc(cx,cy,4,0,Math.PI*2);vizCtx.fillStyle='#fff';vizCtx.shadowColor='#00ffcc';vizCtx.shadowBlur=20;vizCtx.fill();vizCtx.shadowBlur=0}
function updateVizData(contacts){if(!contacts||!contacts.length)return;contactData=[];const step=Math.max(1,Math.floor(contacts.length/64));for(let i=0;i<64;i++){const c=contacts[Math.min(i*step,contacts.length-1)];contactData.push({val:c?(c.status==='sent'?0.8:c.status==='failed'?0.3:0.5):0.1,sent:c?c.status==='sent':false})}}
function pulseViz(){vizPulse+=1.5}