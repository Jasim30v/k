function toggleHistory(){const p=document.getElementById('historyPanel');p.style.display=p.style.display==='none'?'block':'none';document.getElementById('btnHistory').classList.toggle('active',p.style.display==='block');renderHistory()}
function renderHistory(){
    const c=document.getElementById('historyContent');
    const h=loadHistory();
    if(!h.length){c.innerHTML='<p class="history-line">📱 لا يوجد سجل بعد</p><p class="history-line">✨ ابدأ الإرسال لعرض السجل</p>';return}
    c.innerHTML=h.map((e,i)=>{
        const t=new Date(e.time).toLocaleTimeString('ar');
        if(e.type==='load')return '<p class="history-line '+(i===0?'active':'')+'">📁 '+t+' — تم تحميل '+e.count+' جهة</p>';
        if(e.type==='complete')return '<p class="history-line '+(i===0?'active':'')+'">🎉 '+t+' — اكتمل الإرسال ('+e.count+')</p>';
        const cls=e.ok?'':'fail';
        return '<p class="history-line '+cls+' '+(i===0?'active':'')+'">'+(e.ok?'✅':'❌')+' '+t+' — '+escapeHtml(e.name)+' ('+escapeHtml(e.number)+')'+(e.error?' — '+escapeHtml(e.error):'')+'</p>';
    }).join('');
}
function clearHistory(){if(confirm('مسح السجل؟')){saveHistory([]);renderHistory();showToast('🗑 تم مسح السجل')}}
function toggleSettings(){
    const p=document.getElementById('settingsPanel');
    p.style.display=p.style.display==='none'?'block':'none';
    document.getElementById('btnSettings').classList.toggle('active',p.style.display==='block');
    document.getElementById('skipFailed').checked=settings.skipFailed;
    document.getElementById('soundAlert').checked=settings.soundAlert;
    document.getElementById('simulateMode').checked=settings.simulate;
    document.getElementById('senderId').value=settings.senderId||'';
}
function saveSettings(){
    settings.skipFailed=document.getElementById('skipFailed').checked;
    settings.soundAlert=document.getElementById('soundAlert').checked;
    settings.simulate=document.getElementById('simulateMode').checked;
    settings.senderId=document.getElementById('senderId').value.trim();
    saveSettingsToStorage();
    showToast('⚙ تم الحفظ');
}
function saveSettingsToStorage(){saveData(KEYS.settings,settings)}