let currentFilters={type:'all',search:''};
function initFilters(){currentFilters=loadFilters();document.getElementById('searchBox').value=currentFilters.search||'';}
function toggleFilters(){const p=document.getElementById('filterPanel');p.style.display=p.style.display==='none'?'block':'none';document.getElementById('btnFilters').classList.toggle('active',p.style.display==='block')}
function setFilter(type,el){document.querySelectorAll('.filter-presets .preset-btn').forEach(b=>b.classList.remove('active'));el.classList.add('active');currentFilters.type=type;saveFilters(currentFilters);renderContacts()}
function getFilteredContacts(){
    const q=(currentFilters.search||'').toLowerCase();
    return contacts.filter(c=>{
        if(q&&!(c.name.toLowerCase().includes(q)||c.number.toLowerCase().includes(q)))return false;
        switch(currentFilters.type){
            case 'pending':return c.status==='pending';
            case 'sent':return c.status==='sent';
            case 'failed':return c.status==='failed';
            default:return true;
        }
    });
}
document.addEventListener('input',e=>{
    if(e.target.id==='searchBox'){currentFilters.search=e.target.value;saveFilters(currentFilters);renderContacts()}
});