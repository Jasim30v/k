function showToast(msg,isError){
    const t=document.getElementById('toast');
    t.textContent=msg;
    t.classList.toggle('error',!!isError);
    t.classList.add('show');
    clearTimeout(t._timer);
    t._timer=setTimeout(()=>t.classList.remove('show'),2600);
}
function initMessageCounter(){
    const ta=document.getElementById('messageBody');
    const cc=document.getElementById('charCount');
    const pc=document.getElementById('partsCount');
    ta.addEventListener('input',()=>{
        const len=ta.value.length;
        cc.textContent=len+' حرف';
        const parts=Math.max(1,Math.ceil(len/CONFIG.limits.smsLength));
        pc.textContent=parts+' رسالة';
    });
}
(function boot(){
    initParticles();
    initVisualizer();
    initSender();
    initFilters();
    initMessageCounter();
    const savedSettings=loadSettings();
    if(savedSettings.intervalSeconds){
        document.getElementById('intervalSlider').value=savedSettings.intervalSeconds;
        document.getElementById('intervalValue').textContent=savedSettings.intervalSeconds+' ثانية';
    }
    const savedMsg=loadData('smsblaster2044_msg','');
    if(savedMsg){
        document.getElementById('messageBody').value=savedMsg;
        document.getElementById('messageBody').dispatchEvent(new Event('input'));
    }
    document.getElementById('messageBody').addEventListener('input',e=>{
        saveData('smsblaster2044_msg',e.target.value);
    });
    if(!isLiveMode()){
        setTimeout(()=>showToast('🧪 وضع المحاكاة (بدون إرسال حقيقي)'),600);
    }else{
        setTimeout(()=>showToast('🔴 الوضع المباشر — إرسال حقيقي'),600);
    }
    console.log('%c📱 SMS BLASTER 2044 Ready','color:#00ffcc;font-size:16px;font-weight:bold');
})();