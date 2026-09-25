const KEYS={contacts:'smsblaster2044_contacts',settings:'smsblaster2044_settings',history:'smsblaster2044_history',filters:'smsblaster2044_filters',queue:'smsblaster2044_queue'};
function saveData(k,v){try{localStorage.setItem(k,JSON.stringify(v));return 1}catch(e){return 0}}
function loadData(k,d=null){try{const v=localStorage.getItem(k);return v?JSON.parse(v):d}catch(e){return d}}
function saveContacts(list){const data=list.map(c=>({id:c.id,name:c.name,number:c.number,status:c.status,sentAt:c.sentAt||null,failReason:c.failReason||null}));return saveData(KEYS.contacts,data)}
function loadContacts(){return loadData(KEYS.contacts,[])}
function saveQueue(q){saveData(KEYS.queue,q)}
function loadQueue(){return loadData(KEYS.queue,{currentIndex:0,running:false})}
function saveFilters(f){saveData(KEYS.filters,f)}
function loadFilters(){return loadData(KEYS.filters,{type:'all',search:''})}
function saveHistory(h){saveData(KEYS.history,h)}
function loadHistory(){return loadData(KEYS.history,[])}
function addToHistory(entry){const h=loadHistory();h.unshift(entry);if(h.length>CONFIG.limits.maxHistoryEntries)h.pop();saveHistory(h)}
function saveSettings(s){saveData(KEYS.settings,s)}
function loadSettings(){return loadData(KEYS.settings,{...CONFIG.defaults})}