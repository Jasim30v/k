let contacts=[],settings=loadSettings(),currentIndex=0,isRunning=false,nextTimer=null,countdownTimer=null,countdown=0;
function initSender(){
    contacts=loadContacts();
    if(contacts.length)currentIndex=contacts.findIndex(c=>c.status==='pending');
    if(currentIndex<0)currentIndex=0;
    renderContacts();
    updateVizData(contacts);
    updateProgressUI();
}
async function loadContactsFromFile(){
    try{
        const res=await fetch(CONFIG.defaults.contactsFile+'?t='+Date.now());
        if(!res.ok)throw new Error('HTTP '+res.status);
        const text=await res.text();
        const parsed=parseContactsText(text);
        if(!parsed.length){showToast('⚠ الملف فارغ أو غير صالح',true);return}
        contacts=parsed;
        currentIndex=0;
        saveContacts(contacts);
        renderContacts();
        updateVizData(contacts);
        updateProgressUI();
        showToast('✅ تم تحميل '+parsed.length+' جهة اتصال');
        addToHistory({time:new Date().toISOString(),type:'load',count:parsed.length});
        renderHistory();
    }catch(e){
        showToast('❌ فشل قراءة contacts.txt: '+e.message,true);
        console.error(e);
    }
}
function parseContactsText(text){
    const lines=text.split(/\r?\n/).map(l=>l.trim()).filter(l=>l&&!l.startsWith('#'));
    const out=[];
    lines.forEach((line,i)=>{
        const parts=line.split(',').map(p=>p.trim());
        const number=parts[0];
        const name=parts[1]||('جهة '+(i+1));
        if(!number)return;
        out.push({id:'c_'+Date.now()+'_'+i,name:name,number:number,status:'pending',sentAt:null,failReason:null});
    });
    return out;
}
function toggleAutoSend(){
    if(!contacts.length){showToast('⚠ حمّل جهات الاتصال أولاً',true);return}
    if(!document.getElementById('messageBody').value.trim()){showToast('⚠ اكتب نص الرسالة أولاً',true);return}
    if(isRunning)stopAutoSend();
    else startAutoSend();
}
function startAutoSend(){
    isRunning=true;
    const btn=document.getElementById('sendBtn');
    btn.classList.add('running');
    document.getElementById('sendIcon').className='fas fa-pause';
    document.getElementById('sendStatus').textContent='جاري الإرسال...';
    showToast('▶ بدأ الإرسال التسلسلي');
    scheduleNext(0);
}
function stopAutoSend(){
    isRunning=false;
    clearTimeout(nextTimer);
    clearInterval(countdownTimer);
    const btn=document.getElementById('sendBtn');
    btn.classList.remove('running');
    document.getElementById('sendIcon').className='fas fa-play';
    document.getElementById('sendStatus').textContent='متوقف';
    document.getElementById('nextIn').textContent='التالي: --';
    showToast('⏸ تم الإيقاف');
}
function scheduleNext(delayMs){
    clearTimeout(nextTimer);
    clearInterval(countdownTimer);
    if(delayMs>0){
        countdown=Math.ceil(delayMs/1000);
        document.getElementById('nextIn').textContent='التالي: '+countdown+'ث';
        countdownTimer=setInterval(()=>{
            countdown--;
            if(countdown>0)document.getElementById('nextIn').textContent='التالي: '+countdown+'ث';
        },1000);
    }
    nextTimer=setTimeout(()=>{sendNextInQueue()},delayMs);
}
async function sendNextInQueue(){
    if(!isRunning)return;
    while(currentIndex<contacts.length && contacts[currentIndex].status==='sent'){
        currentIndex++;
    }
    if(currentIndex>=contacts.length){
        stopAutoSend();
        showToast('🎉 اكتمل إرسال جميع الرسائل');
        addToHistory({time:new Date().toISOString(),type:'complete',count:contacts.length});
        renderHistory();
        return;
    }
    const contact=contacts[currentIndex];
    document.getElementById('currentContact').textContent=contact.name+' • '+contact.number;
    document.getElementById('sendStatus').textContent='⏳ جاري الإرسال...';
    const message=document.getElementById('messageBody').value.trim();
    let result;
    if(isLiveMode()){
        result=await sendViaAPI(contact,message);
    }else{
        result=await simulateSend(contact,message);
    }
    if(result.ok){
        contact.status='sent';
        contact.sentAt=new Date().toISOString();
        contact.failReason=null;
        document.getElementById('sendStatus').textContent='✅ تم الإرسال';
        showToast('✅ أُرسلت إلى '+contact.name);
        addToHistory({time:contact.sentAt,type:'sent',name:contact.name,number:contact.number,ok:true});
        pulseViz();
        if(settings.soundAlert)playBeep(880);
    }else{
        contact.status='failed';
        contact.failReason=result.error||'فشل الإرسال';
        document.getElementById('sendStatus').textContent='❌ فشل الإرسال';
        showToast('❌ فشل: '+contact.name+' — '+contact.failReason,true);
        addToHistory({time:new Date().toISOString(),type:'sent',name:contact.name,number:contact.number,ok:false,error:contact.failReason});
        if(settings.soundAlert)playBeep(220);
        if(!settings.skipFailed){
            stopAutoSend();
            saveContacts(contacts);
            renderContacts();
            renderHistory();
            return;
        }
    }
    saveContacts(contacts);
    renderContacts();
    updateVizData(contacts);
    updateProgressUI();
    renderHistory();
    currentIndex++;
    saveQueue({currentIndex,running:true});
    if(isRunning)scheduleNext(settings.intervalSeconds*1000);
}
async function sendNextNow(){
    if(!isRunning){toggleAutoSend();return}
    clearTimeout(nextTimer);
    clearInterval(countdownTimer);
    await sendNextInQueue();
}
async function sendViaAPI(contact,message){
    try{
        if(CONFIG.backend.enabled){
            const res=await fetch(CONFIG.backend.url,{
                method:'POST',
                headers:{'Content-Type':'application/json','Authorization':'Bearer '+CONFIG.backend.apiKey},
                body:JSON.stringify({to:contact.number,body:message,from:CONFIG.twilio.fromNumber||CONFIG.defaults.senderId})
            });
            if(!res.ok)throw new Error('HTTP '+res.status);
            return {ok:true};
        }
        const accountSid=CONFIG.twilio.accountSid;
        const authToken=CONFIG.twilio.authToken;
        const fromNumber=CONFIG.twilio.fromNumber;
        const endpoint=CONFIG.twilio.endpoint;
        const url=endpoint+'/'+accountSid+'/Messages.json';
        const body=new URLSearchParams({To:contact.number,From:fromNumber,Body:message});
        const res=await fetch(url,{
            method:'POST',
            headers:{'Authorization':'Basic '+btoa(accountSid+':'+authToken),'Content-Type':'application/x-www-form-urlencoded'},
            body:body.toString()
        });
        if(!res.ok)throw new Error('Twilio '+res.status);
        return {ok:true};
    }catch(e){
        return {ok:false,error:e.message};
    }
}
function simulateSend(contact,message){
    return new Promise(resolve=>{
        setTimeout(()=>{
            const ok=Math.random()>0.1;
            resolve(ok?{ok:true}:{ok:false,error:'محاكاة: فشل عشوائي'});
        },600+Math.random()*400);
    });
}
function renderContacts(){
    const c=document.getElementById('contactsList');
    if(!contacts.length){
        c.innerHTML='<div class="empty-playlist"><span>📁</span><p>اضغط زر التحميل لقراءة contacts.txt</p></div>';
        document.getElementById('contactsStats').textContent='0 جهة';
        return;
    }
    const filtered=getFilteredContacts();
    document.getElementById('contactsStats').textContent=filtered.length+' / '+contacts.length;
    if(!filtered.length){
        c.innerHTML='<div class="empty-playlist"><span>🔍</span><p>لا نتائج مطابقة</p></div>';
        return;
    }
    c.innerHTML=filtered.map(ct=>{
        const idx=contacts.indexOf(ct);
        const isCurrent=idx===currentIndex&&isRunning;
        const cls=['contact-item',ct.status==='sent'?'sent':'',ct.status==='failed'?'failed':'',isCurrent?'active':''].filter(Boolean).join(' ');
        const statusLabel=ct.status==='sent'?'✓ مرسل':ct.status==='failed'?'✗ فشل':'⏳ متبقي';
        return '<div class="'+cls+'" onclick="focusContact('+idx+')">'+
            '<div class="c-icon">'+(ct.status==='sent'?'✅':ct.status==='failed'?'❌':'👤')+'</div>'+
            '<div class="c-info">'+
                '<div class="c-name">'+escapeHtml(ct.name)+'</div>'+
                '<div class="c-number">'+escapeHtml(ct.number)+'</div>'+
            '</div>'+
            '<span class="c-status '+ct.status+'">'+statusLabel+'</span>'+
        '</div>';
    }).join('');
}
function focusContact(idx){
    const ct=contacts[idx];
    if(!ct)return;
    document.getElementById('currentContact').textContent=ct.name+' • '+ct.number;
    showToast('📌 '+ct.name);
}
function updateProgressUI(){
    const total=contacts.length;
    const sent=contacts.filter(c=>c.status==='sent').length;
    const failed=contacts.filter(c=>c.status==='failed').length;
    const pending=total-sent-failed;
    document.getElementById('progressText').textContent=(sent+failed)+' / '+total;
    document.getElementById('currentContact').textContent=total?(pending+' متبقي • '+sent+' مرسل'):'لا يوجد';
}
function updateInterval(){
    const v=parseInt(document.getElementById('intervalSlider').value);
    settings.intervalSeconds=v;
    document.getElementById('intervalValue').textContent=v+' ثانية';
    saveSettings(settings);
}
function resetQueue(){
    if(!confirm('إعادة تعيين كل حالات الإرسال؟'))return;
    contacts.forEach(c=>{c.status='pending';c.sentAt=null;c.failReason=null});
    currentIndex=0;
    saveContacts(contacts);
    saveQueue({currentIndex:0,running:false});
    stopAutoSend();
    renderContacts();
    updateVizData(contacts);
    updateProgressUI();
    showToast('🔄 تم إعادة التعيين');
}
function exportData(){
    const data={exportedAt:new Date().toISOString(),message:document.getElementById('messageBody').value,interval:settings.intervalSeconds,contacts:contacts,history:loadHistory()};
    const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
    const url=URL.createObjectURL(blob);
    const a=document.createElement('a');a.href=url;a.download='sms_report_'+Date.now()+'.json';a.click();
    URL.revokeObjectURL(url);
    showToast('📥 تم التصدير');
}
function escapeHtml(s){return String(s).replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]))}
function playBeep(freq){try{const ctx=new (window.AudioContext||window.webkitAudioContext)();const o=ctx.createOscillator();const g=ctx.createGain();o.connect(g);g.connect(ctx.destination);o.frequency.value=freq;o.type='sine';g.gain.setValueAtTime(0.08,ctx.currentTime);g.gain.exponentialRampToValueAtTime(0.001,ctx.currentTime+0.15);o.start();o.stop(ctx.currentTime+0.15)}catch(e){}}
function loadContacts(){loadContactsFromFile()}