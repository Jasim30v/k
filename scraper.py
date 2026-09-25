#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║                                                            ║
║  📞  AUTO DIALER 2044 - ULTIMATE SEQUENTIAL CALLER  📞    ║
║     Ultimate Generator - 14 Files - 3000+ Lines            ║
║                                                            ║
║  🌐  3D Contact Visualizer + Live Call Progress           ║
║  🎨  Futuristic Glass Morphism Design                      ║
║  💾  Call History with Local Storage                      ║
║  📊  Real-time Call Monitoring                            ║
║  🔄  Auto Sequential Calling with Custom Timer            ║
║  📁  Load Contacts from TXT File                          ║
║  ☎   Real SIM Calls (via Cordova APK)                    ║
║                                                            ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import json

TOTAL_LINES = 0

def write(filename, content):
    global TOTAL_LINES
    os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    lines = content.count('\n') + 1
    TOTAL_LINES += lines
    print(f"  ✅ {filename} ({lines} سطر)")

def section(title):
    print(f"\n{'='*60}")
    print(f"  📞 {title}")
    print(f"{'='*60}")

# ═══════════════════════════════════════════════════════════
# 📞 1. index.html
# ═══════════════════════════════════════════════════════════

def build_index():
    return """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>📞 Auto Dialer 2044</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700;800;900&family=Orbitron:wght@400;600;700;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="bg-void"></div>
    <div class="bg-ring bg-ring-1"></div>
    <div class="bg-ring bg-ring-2"></div>
    <div class="bg-ring bg-ring-3"></div>
    <div id="particlesContainer"></div>

    <div class="app">
        <div class="header">
            <div class="header-left">
                <div class="logo">📞</div>
                <div class="header-text">
                    <h1>Auto Dialer 2044</h1>
                    <span>✦ Ultimate Caller ✦</span>
                </div>
            </div>
            <div class="header-right">
                <button class="btn-icon" onclick="toggleFilters()" id="btnFilters"><i class="fas fa-filter"></i></button>
                <button class="btn-icon" onclick="toggleHistory()" id="btnHistory"><i class="fas fa-history"></i></button>
                <button class="btn-icon" onclick="toggleSettings()" id="btnSettings"><i class="fas fa-cog"></i></button>
            </div>
        </div>

        <!-- Call Status Banner -->
        <div class="call-banner" id="callBanner" style="display:none">
            <div class="call-pulse"></div>
            <div class="call-info">
                <div class="call-label">📞 جاري الاتصال</div>
                <div class="call-name" id="callName">-</div>
                <div class="call-number" id="callNumber">-</div>
            </div>
            <div class="call-timer" id="callTimer">00:00</div>
        </div>

        <!-- 3D Visualizer -->
        <div class="visualizer-3d" id="visualizer3D">
            <canvas id="vizCanvas"></canvas>
            <div class="viz-overlay">
                <div class="track-info">
                    <div class="track-title" id="currentContact">لا يوجد</div>
                    <div class="track-artist" id="callStatus">جاهز للاتصال</div>
                </div>
                <div class="track-time">
                    <span id="progressText">0 / 0</span>
                    <span id="nextIn">التالي: --</span>
                </div>
            </div>
        </div>

        <!-- Call Duration Control -->
        <div class="timer-box">
            <label>⏱ مدة كل مكالمة (ثواني)</label>
            <input type="range" class="gold-slider" id="durationSlider" min="3" max="120" value="5" oninput="updateDuration()">
            <div class="timer-labels">
                <span id="durationValue">5 ثوانٍ</span>
                <span id="durationHint">المدة بين كل اتصال</span>
            </div>
        </div>

        <!-- Gap Between Calls -->
        <div class="timer-box">
            <label>⏳ الفاصل بين المكالمات (ثواني)</label>
            <input type="range" class="gold-slider" id="gapSlider" min="1" max="30" value="3" oninput="updateGap()">
            <div class="timer-labels">
                <span id="gapValue">3 ثوانٍ</span>
                <span id="gapHint">بعد إنهاء كل مكالمة</span>
            </div>
        </div>

        <!-- Controls -->
        <div class="controls">
            <button class="ctrl-btn" onclick="loadContacts()" title="تحميل الملف"><i class="fas fa-file-import"></i></button>
            <button class="ctrl-btn" onclick="resetQueue()" title="إعادة تعيين"><i class="fas fa-undo"></i></button>
            <button class="ctrl-play" id="callBtn" onclick="toggleAutoCall()"><i class="fas fa-phone" id="callIcon"></i></button>
            <button class="ctrl-btn" onclick="callNextNow()" title="الاتصال التالي فوراً"><i class="fas fa-forward"></i></button>
            <button class="ctrl-btn" onclick="exportData()" title="تصدير"><i class="fas fa-download"></i></button>
        </div>

        <!-- Filters Panel -->
        <div class="filter-panel" id="filterPanel" style="display:none">
            <div class="filter-header">
                <h3>🔍 Filters</h3>
                <div class="filter-presets">
                    <button class="preset-btn active" onclick="setFilter('all', this)">الكل</button>
                    <button class="preset-btn" onclick="setFilter('pending', this)">متبقي</button>
                    <button class="preset-btn" onclick="setFilter('called', this)">تم الاتصال</button>
                    <button class="preset-btn" onclick="setFilter('failed', this)">فشل</button>
                </div>
            </div>
            <div class="filter-options">
                <div class="filter-knob">
                    <span>🔍 بحث</span>
                    <input type="text" id="searchBox" class="search-input" placeholder="اسم أو رقم..." oninput="renderContacts()">
                </div>
            </div>
        </div>

        <!-- Settings Panel -->
        <div class="settings-panel" id="settingsPanel" style="display:none">
            <div class="filter-header">
                <h3>⚙ الإعدادات</h3>
            </div>
            <div class="setting-row">
                <span>🔄 تجاوز الفاشلة</span>
                <input type="checkbox" id="skipFailed" onchange="saveSettings()">
            </div>
            <div class="setting-row">
                <span>🔔 تنبيه صوتي</span>
                <input type="checkbox" id="soundAlert" checked onchange="saveSettings()">
            </div>
            <div class="setting-row">
                <span>🧪 وضع المحاكاة</span>
                <input type="checkbox" id="simulateMode" checked onchange="saveSettings()">
            </div>
            <div class="setting-row">
                <span>📞 فتح لوحة الاتصال</span>
                <input type="checkbox" id="openDialer" checked onchange="saveSettings()">
            </div>
        </div>

        <!-- History Panel -->
        <div class="history-panel" id="historyPanel" style="display:none">
            <div class="history-header">
                <h3>📜 سجل الاتصالات</h3>
                <button class="btn-action" onclick="clearHistory()">🗑 مسح</button>
            </div>
            <div class="history-content" id="historyContent">
                <p class="history-line">📞 لا يوجد سجل بعد</p>
                <p class="history-line">✨ ابدأ الاتصال لعرض السجل</p>
            </div>
        </div>

        <!-- Contacts List -->
        <div class="playlist-section">
            <div class="playlist-header">
                <h3>👥 جهات الاتصال</h3>
                <span class="network-stats" id="contactsStats">0 جهة</span>
            </div>
            <div class="playlist" id="contactsList">
                <div class="empty-playlist">
                    <span>📁</span>
                    <p>اضغط زر التحميل لقراءة ملف contacts.txt</p>
                </div>
            </div>
        </div>
    </div>

    <div class="toast" id="toast"></div>

    <script src="config.js"></script>
    <script src="storage.js"></script>
    <script src="particles.js"></script>
    <script src="visualizer.js"></script>
    <script src="dialer.js"></script>
    <script src="filters.js"></script>
    <script src="history.js"></script>
    <script src="app.js"></script>
</body>
</html>"""

# ═══════════════════════════════════════════════════════════
# 📞 2. style.css
# ═══════════════════════════════════════════════════════════

def build_style():
    return """*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#050510;--card:rgba(10,10,30,0.85);--card2:rgba(15,15,40,0.7);--text:#e8e0f0;--text2:#9088a8;--text3:#504868;--accent:#00ffcc;--accent2:#ff44aa;--accent3:#ffaa00;--accent4:#6366f1;--glass:rgba(0,255,204,0.06);--border:rgba(0,255,204,0.12);--radius:24px;--radius-sm:16px;--radius-xs:12px;--green:#00ff88;--red:#ff3355}
body{font-family:'Cairo',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;overflow-x:hidden;-webkit-tap-highlight-color:transparent;direction:rtl;user-select:none}
.bg-void{position:fixed;inset:0;z-index:0;background:radial-gradient(ellipse at 30% 20%,rgba(0,255,204,0.04) 0%,transparent 60%),radial-gradient(ellipse at 70% 80%,rgba(255,68,170,0.03) 0%,transparent 60%),var(--bg)}
.bg-ring{position:fixed;border-radius:50%;border:1px solid rgba(0,255,204,0.06);z-index:0;pointer-events:none;animation:ringRotate 30s linear infinite}
.bg-ring-1{width:600px;height:600px;top:-200px;left:-100px;animation-duration:25s}
.bg-ring-2{width:500px;height:500px;bottom:-150px;right:-80px;animation-duration:35s;animation-direction:reverse}
.bg-ring-3{width:400px;height:400px;top:30%;left:40%;animation-duration:40s}
@keyframes ringRotate{to{transform:rotate(360deg)}}
.app{width:100%;max-width:520px;margin:0 auto;padding:12px;position:relative;z-index:1}
.header{display:flex;align-items:center;justify-content:space-between;padding:12px 16px;background:var(--card);backdrop-filter:blur(40px);border-radius:var(--radius);border:1px solid var(--border);margin-bottom:12px}
.header-left{display:flex;align-items:center;gap:10px}
.logo{width:46px;height:46px;background:var(--glass);border:1px solid var(--border);border-radius:var(--radius-sm);display:flex;align-items:center;justify-content:center;font-size:24px;animation:logoGlow 3s ease-in-out infinite}
@keyframes logoGlow{0%,100%{box-shadow:0 0 20px rgba(0,255,204,0.3)}50%{box-shadow:0 0 35px rgba(255,68,170,0.6)}}
.header-text h1{font-family:'Orbitron',sans-serif;font-size:18px;font-weight:800;background:linear-gradient(135deg,#00ffcc,#6366f1);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.header-text span{font-size:7px;color:var(--text3);letter-spacing:3px}
.header-right{display:flex;gap:6px}
.btn-icon{width:38px;height:38px;background:var(--card2);border:1px solid var(--border);border-radius:var(--radius-xs);display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:15px;color:var(--text2);transition:all 0.3s}
.btn-icon:hover{border-color:var(--accent);color:var(--accent)}
.btn-icon.active{background:var(--glass);border-color:var(--accent);color:var(--accent);box-shadow:0 0 20px rgba(0,255,204,0.3)}

/* Call Banner */
.call-banner{position:relative;display:flex;align-items:center;gap:12px;background:linear-gradient(135deg,rgba(0,255,136,0.15),rgba(0,255,204,0.08));border:1px solid var(--green);border-radius:var(--radius-sm);padding:12px 16px;margin-bottom:10px;overflow:hidden}
.call-pulse{position:absolute;left:12px;top:50%;transform:translateY(-50%);width:12px;height:12px;background:var(--green);border-radius:50%;box-shadow:0 0 0 0 rgba(0,255,136,0.7);animation:callPulse 1.5s infinite}
@keyframes callPulse{0%{box-shadow:0 0 0 0 rgba(0,255,136,0.7)}70%{box-shadow:0 0 0 15px rgba(0,255,136,0)}100%{box-shadow:0 0 0 0 rgba(0,255,136,0)}}
.call-info{flex:1;padding-right:22px}
.call-label{font-size:9px;color:var(--green);font-weight:700;letter-spacing:1px}
.call-name{font-size:14px;font-weight:700;color:var(--text);margin-top:2px}
.call-number{font-size:11px;color:var(--text2);direction:ltr;text-align:right}
.call-timer{font-family:'Orbitron',sans-serif;font-size:18px;font-weight:800;color:var(--green);text-shadow:0 0 15px rgba(0,255,136,0.6)}

.visualizer-3d{position:relative;width:100%;aspect-ratio:1;max-height:350px;background:var(--card);backdrop-filter:blur(40px);border-radius:var(--radius);border:1px solid var(--border);overflow:hidden;margin-bottom:10px}
.visualizer-3d canvas{width:100%;height:100%}
.viz-overlay{position:absolute;bottom:0;left:0;right:0;padding:16px;background:linear-gradient(to top,rgba(5,5,16,0.9),transparent)}
.track-title{font-family:'Orbitron',sans-serif;font-size:16px;font-weight:700;color:var(--accent);margin-bottom:2px;text-shadow:0 0 20px rgba(0,255,204,0.5);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.track-artist{font-size:11px;color:var(--text2)}
.track-time{display:flex;justify-content:space-between;font-family:'Orbitron',sans-serif;font-size:10px;color:var(--accent2);margin-top:6px}

.timer-box{background:var(--card);backdrop-filter:blur(40px);border-radius:var(--radius);border:1px solid var(--border);padding:12px 16px;margin-bottom:10px;display:flex;flex-direction:column;gap:8px}
.timer-box label{font-size:11px;color:var(--text2);font-weight:600}
.timer-labels{display:flex;justify-content:space-between;align-items:center;font-size:9px}
.timer-labels span:first-child{color:var(--accent);font-family:'Orbitron',sans-serif;font-weight:700;font-size:11px}
.timer-labels span:last-child{color:var(--text3)}

.controls{display:flex;align-items:center;justify-content:center;gap:16px;margin-bottom:12px}
.ctrl-btn{width:42px;height:42px;background:var(--card2);border:1px solid var(--border);border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:15px;color:var(--text2);transition:all 0.3s}
.ctrl-btn:hover{border-color:var(--accent);color:var(--accent)}
.ctrl-btn.active{border-color:var(--accent);color:var(--accent);box-shadow:0 0 20px rgba(0,255,204,0.3)}
.ctrl-play{width:60px;height:60px;background:linear-gradient(135deg,var(--green),var(--accent));border:none;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:22px;color:#000;box-shadow:0 8px 30px rgba(0,255,136,0.4);transition:all 0.3s}
.ctrl-play:hover{transform:scale(1.05);box-shadow:0 12px 40px rgba(0,255,136,0.6)}
.ctrl-play:active{transform:scale(0.95)}
.ctrl-play.running{background:linear-gradient(135deg,#ff4466,#ff44aa);animation:pulseBtn 1.5s ease-in-out infinite}
@keyframes pulseBtn{0%,100%{box-shadow:0 0 20px rgba(255,68,102,0.5)}50%{box-shadow:0 0 45px rgba(255,68,170,0.9)}}

.filter-panel,.settings-panel{background:var(--card);backdrop-filter:blur(40px);border-radius:var(--radius);border:1px solid var(--border);padding:16px;margin-bottom:12px;animation:slideDown 0.4s ease}
@keyframes slideDown{from{opacity:0;max-height:0}to{opacity:1;max-height:800px}}
.filter-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;flex-wrap:wrap;gap:8px}
.filter-header h3{font-family:'Orbitron',sans-serif;font-size:13px;font-weight:700;color:var(--accent)}
.filter-presets{display:flex;gap:4px;flex-wrap:wrap}
.preset-btn{padding:5px 10px;background:var(--card2);border:1px solid var(--border);color:var(--text2);cursor:pointer;border-radius:15px;font-size:9px;font-family:'Cairo',sans-serif;transition:all 0.3s}
.preset-btn.active{background:var(--accent);border-color:var(--accent);color:#000;font-weight:700}
.filter-options{display:flex;gap:20px;justify-content:center;flex-wrap:wrap}
.filter-knob{display:flex;flex-direction:column;align-items:center;gap:4px;width:100%}
.filter-knob span{font-size:9px;color:var(--text2)}
.search-input{width:100%;padding:8px 12px;background:var(--card2);border:1px solid var(--border);border-radius:var(--radius-xs);color:var(--text);font-family:'Cairo',sans-serif;font-size:12px;outline:none}
.search-input:focus{border-color:var(--accent)}

.gold-slider{width:100%;height:4px;-webkit-appearance:none;appearance:none;background:rgba(0,255,204,0.15);border-radius:2px;outline:none;cursor:pointer}
.gold-slider::-webkit-slider-thumb{-webkit-appearance:none;width:20px;height:20px;background:var(--accent);border-radius:50%;cursor:pointer;box-shadow:0 0 15px rgba(0,255,204,0.6);border:2px solid #000}

.setting-row{display:flex;align-items:center;justify-content:space-between;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.04)}
.setting-row span{font-size:11px;color:var(--text2)}
.setting-row input[type=checkbox]{width:20px;height:20px;accent-color:var(--accent);cursor:pointer}

.history-panel{background:var(--card);backdrop-filter:blur(40px);border-radius:var(--radius);border:1px solid var(--border);padding:16px;margin-bottom:12px;max-height:220px;overflow-y:auto;animation:slideDown 0.4s ease}
.history-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px}
.history-header h3{font-family:'Orbitron',sans-serif;font-size:13px;font-weight:700;color:var(--accent2)}
.history-line{padding:6px 0;font-size:12px;color:var(--text2);text-align:center;transition:all 0.3s;border-bottom:1px solid rgba(255,255,255,0.03)}
.history-line.active{color:var(--accent);font-size:14px;font-weight:700;text-shadow:0 0 15px rgba(0,255,204,0.4)}
.history-line.fail{color:#ff4466}

.playlist-section{margin-top:8px;padding-bottom:30px}
.playlist-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px}
.playlist-header h3{font-family:'Orbitron',sans-serif;font-size:13px;font-weight:700;color:var(--text)}
.network-stats{font-size:10px;color:var(--accent);font-family:'Orbitron',sans-serif}
.btn-action{padding:7px 14px;background:var(--card2);border:1px solid var(--border);color:var(--accent);cursor:pointer;border-radius:20px;font-size:10px;font-family:'Cairo',sans-serif;transition:all 0.3s}
.btn-action:hover{border-color:var(--accent);box-shadow:0 0 15px rgba(0,255,204,0.2)}
.playlist{display:flex;flex-direction:column;gap:5px;max-height:400px;overflow-y:auto}
.contact-item{display:flex;align-items:center;gap:10px;padding:10px 12px;background:var(--card2);border:1px solid var(--border);border-radius:var(--radius-sm);cursor:pointer;transition:all 0.3s}
.contact-item:hover{border-color:var(--accent);background:var(--glass)}
.contact-item.active{border-color:var(--green);background:rgba(0,255,136,0.08);box-shadow:0 0 15px rgba(0,255,136,0.2);animation:activeGlow 1.5s infinite}
@keyframes activeGlow{0%,100%{box-shadow:0 0 15px rgba(0,255,136,0.2)}50%{box-shadow:0 0 30px rgba(0,255,136,0.5)}}
.contact-item.called{opacity:0.55;border-color:rgba(0,255,204,0.4)}
.contact-item.called .c-name::after{content:' ✓';color:var(--accent)}
.contact-item.failed{border-color:rgba(255,68,102,0.5)}
.contact-item.failed .c-name::after{content:' ✗';color:#ff4466}
.contact-item .c-icon{font-size:20px;width:28px;text-align:center}
.contact-item .c-info{flex:1;min-width:0}
.contact-item .c-name{font-size:12px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.contact-item .c-number{font-size:10px;color:var(--text3);direction:ltr;text-align:right}
.contact-item .c-status{font-size:9px;padding:3px 8px;border-radius:10px;background:var(--card);color:var(--text3)}
.contact-item .c-status.called{color:var(--accent);border:1px solid var(--accent)}
.contact-item .c-status.failed{color:#ff4466;border:1px solid #ff4466}
.contact-item .c-call{background:var(--green);color:#000;border:none;width:32px;height:32px;border-radius:50%;cursor:pointer;font-size:12px;display:flex;align-items:center;justify-content:center;transition:0.3s}
.contact-item .c-call:hover{transform:scale(1.1);box-shadow:0 0 15px rgba(0,255,136,0.5)}
.empty-playlist{text-align:center;padding:30px;color:var(--text3)}
.empty-playlist span{font-size:40px;display:block;margin-bottom:8px}

.toast{position:fixed;bottom:35px;left:50%;transform:translateX(-50%) translateY(130px);background:var(--card);border:1px solid var(--accent);color:var(--text);padding:10px 22px;border-radius:25px;font-size:11px;z-index:300;transition:transform 0.4s cubic-bezier(0.175,0.885,0.32,1.275);font-family:'Cairo',sans-serif;max-width:90%}
.toast.show{transform:translateX(-50%) translateY(0)}
.toast.error{border-color:#ff4466;color:#ff4466}
.particle{position:fixed;border-radius:50%;pointer-events:none;z-index:0}
@keyframes particleFloat{0%{transform:translateY(110vh) scale(0);opacity:0}15%{opacity:0.7}85%{opacity:0.1}100%{transform:translateY(-10vh) scale(1.5);opacity:0}}

@media(max-width:400px){.controls{gap:10px}.filter-options{gap:10px}}"""

# ═══════════════════════════════════════════════════════════
# 📞 3. config.js
# ═══════════════════════════════════════════════════════════

def build_config_js():
    return """// AUTO DIALER 2044 - Configuration
const CONFIG = {
    defaults: {
        callDuration: 5,
        gapBetween: 3,
        contactsFile: 'contacts.txt',
        simulate: true,
        soundAlert: true,
        skipFailed: false,
        openDialer: true
    },
    limits: {
        minDuration: 3,
        maxDuration: 120,
        minGap: 1,
        maxGap: 30,
        maxHistoryEntries: 200
    }
};

// هل نحن داخل Cordova (APK حقيقي)؟
function isCordova(){
    return typeof window !== 'undefined' && window.cordova !== undefined;
}

// هل يمكن الاتصال الحقيقي؟
function canRealCall(){
    return isCordova() && window.cordova && window.cordova.plugins && window.cordova.plugins.CallNumber;
}

// الوضع المباشر = Cordova + عدم المحاكاة
function isLiveMode(){
    return canRealCall() && !CONFIG.defaults.simulate;
}"""

# ═══════════════════════════════════════════════════════════
# 📞 4. storage.js
# ═══════════════════════════════════════════════════════════

def build_storage_js():
    return """const KEYS={contacts:'autodialer2044_contacts',settings:'autodialer2044_settings',history:'autodialer2044_history',filters:'autodialer2044_filters',queue:'autodialer2044_queue'};
function saveData(k,v){try{localStorage.setItem(k,JSON.stringify(v));return 1}catch(e){return 0}}
function loadData(k,d){if(d===undefined)d=null;try{const v=localStorage.getItem(k);return v?JSON.parse(v):d}catch(e){return d}}
function saveContacts(list){const data=list.map(c=>({id:c.id,name:c.name,number:c.number,status:c.status,calledAt:c.calledAt||null,failReason:c.failReason||null}));return saveData(KEYS.contacts,data)}
function loadContacts(){return loadData(KEYS.contacts,[])}
function saveQueue(q){saveData(KEYS.queue,q)}
function loadQueue(){return loadData(KEYS.queue,{currentIndex:0,running:false})}
function saveFilters(f){saveData(KEYS.filters,f)}
function loadFilters(){return loadData(KEYS.filters,{type:'all',search:''})}
function saveHistory(h){saveData(KEYS.history,h)}
function loadHistory(){return loadData(KEYS.history,[])}
function addToHistory(entry){const h=loadHistory();h.unshift(entry);if(h.length>CONFIG.limits.maxHistoryEntries)h.pop();saveHistory(h)}
function saveSettings(s){saveData(KEYS.settings,s)}
function loadSettings(){const s=loadData(KEYS.settings,{});return Object.assign({},CONFIG.defaults,s)}"""

# ═══════════════════════════════════════════════════════════
# 📞 5. particles.js
# ═══════════════════════════════════════════════════════════

def build_particles_js():
    return """function initParticles(){const c=document.getElementById('particlesContainer');c.innerHTML='';const cols=['#00ffcc','#ff44aa','#6366f1'];for(let i=0;i<40;i++){const p=document.createElement('div');p.className='particle';p.style.cssText='left:'+(Math.random()*100)+'%;bottom:-10px;width:'+(Math.random()*4+1)+'px;height:'+(Math.random()*4+1)+'px;background:radial-gradient(circle,'+cols[i%3]+' 0%,transparent 70%);animation:particleFloat '+(Math.random()*5+5)+'s ease-in infinite;animation-delay:'+(Math.random()*5)+'s';c.appendChild(p)}}"""

# ═══════════════════════════════════════════════════════════
# 📞 6. visualizer.js
# ═══════════════════════════════════════════════════════════

def build_visualizer_js():
    return """let vizCanvas,vizCtx,vizAnimationId,contactData=[],vizPulse=0,vizCalling=false;
function initVisualizer(){vizCanvas=document.getElementById('vizCanvas');vizCtx=vizCanvas.getContext('2d');resizeViz();window.addEventListener('resize',resizeViz);for(let i=0;i<64;i++)contactData.push({val:0.1,called:false});drawViz()}
function resizeViz(){const c=vizCanvas.parentElement;if(!c)return;vizCanvas.width=c.clientWidth;vizCanvas.height=c.clientHeight}
function drawViz(){vizAnimationId=requestAnimationFrame(drawViz);const w=vizCanvas.width,h=vizCanvas.height;vizCtx.fillStyle='rgba(5,5,16,0.25)';vizCtx.fillRect(0,0,w,h);const cx=w/2,cy=h/2,r=Math.min(w,h)*0.35;vizPulse+=0.05;
for(let i=0;i<contactData.length;i++){const d=contactData[i];const a=(i/contactData.length)*Math.PI*2+vizPulse*0.1;const rad=r+d.val*40;const x=cx+Math.cos(a)*rad;const y=cy+Math.sin(a)*rad;const col=d.called?'0,255,204':(vizCalling&&i%2===0?'0,255,136':'99,102,241');
vizCtx.beginPath();vizCtx.moveTo(cx,cy);vizCtx.lineTo(x,y);vizCtx.strokeStyle='rgba('+col+','+(0.05+d.val*0.3)+')';vizCtx.lineWidth=0.5+d.val*1.5;vizCtx.stroke();
vizCtx.beginPath();vizCtx.arc(x,y,1.5+d.val*6,0,Math.PI*2);vizCtx.fillStyle='rgba('+col+','+(0.4+d.val*0.6)+')';vizCtx.fill()}
const pulseR=8+Math.sin(vizPulse*2)*3;vizCtx.beginPath();vizCtx.arc(cx,cy,pulseR,0,Math.PI*2);const g=vizCtx.createRadialGradient(cx,cy,0,cx,cy,pulseR*3);g.addColorStop(0,vizCalling?'rgba(0,255,136,0.9)':'rgba(0,255,204,0.8)');g.addColorStop(1,'rgba(0,255,204,0)');vizCtx.fillStyle=g;vizCtx.fill();
vizCtx.beginPath();vizCtx.arc(cx,cy,4,0,Math.PI*2);vizCtx.fillStyle='#fff';vizCtx.shadowColor=vizCalling?'#00ff88':'#00ffcc';vizCtx.shadowBlur=20;vizCtx.fill();vizCtx.shadowBlur=0}
function updateVizData(contacts){if(!contacts||!contacts.length)return;contactData=[];const step=Math.max(1,Math.floor(contacts.length/64));for(let i=0;i<64;i++){const c=contacts[Math.min(i*step,contacts.length-1)];contactData.push({val:c?(c.status==='called'?0.8:c.status==='failed'?0.3:0.5):0.1,called:c?c.status==='called':false})}}
function pulseViz(){vizPulse+=1.5}
function setVizCalling(v){vizCalling=v}"""

# ═══════════════════════════════════════════════════════════
# 📞 7. dialer.js  ← الملف الأساسي (منطق الاتصال)
# ═══════════════════════════════════════════════════════════

def build_dialer_js():
    return """let contacts=[],settings=loadSettings(),currentIndex=0,isRunning=false,nextTimer=null,countdownTimer=null,callTimer=null,callSeconds=0,countdown=0;

// ═══════ التهيئة ═══════
function initDialer(){
    contacts=loadContacts();
    if(contacts.length)currentIndex=contacts.findIndex(c=>c.status==='pending');
    if(currentIndex<0)currentIndex=0;
    renderContacts();
    updateVizData(contacts);
    updateProgressUI();
}

// ═══════ قراءة ملف contacts.txt ═══════
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
    const lines=text.split(/\\r?\\n/).map(function(l){return l.trim()}).filter(function(l){return l&&!l.startsWith('#')});
    const out=[];
    lines.forEach(function(line,i){
        const parts=line.split(',').map(function(p){return p.trim()});
        const number=parts[0];
        const name=parts[1]||('جهة '+(i+1));
        if(!number)return;
        out.push({id:'c_'+Date.now()+'_'+i,name:name,number:number,status:'pending',calledAt:null,failReason:null});
    });
    return out;
}

// ═══════ التشغيل / الإيقاف ═══════
function toggleAutoCall(){
    if(!contacts.length){showToast('⚠ حمّل جهات الاتصال أولاً',true);return}
    if(isRunning)stopAutoCall();
    else startAutoCall();
}

function startAutoCall(){
    isRunning=true;
    const btn=document.getElementById('callBtn');
    btn.classList.add('running');
    document.getElementById('callIcon').className='fas fa-phone-slash';
    document.getElementById('callStatus').textContent='جاري الاتصال التسلسلي...';
    showToast('▶ بدأ الاتصال التسلسلي');
    scheduleNext(0);
}

function stopAutoCall(){
    isRunning=false;
    clearTimeout(nextTimer);
    clearInterval(countdownTimer);
    clearInterval(callTimer);
    const btn=document.getElementById('callBtn');
    btn.classList.remove('running');
    document.getElementById('callIcon').className='fas fa-phone';
    document.getElementById('callStatus').textContent='متوقف';
    document.getElementById('nextIn').textContent='التالي: --';
    document.getElementById('callBanner').style.display='none';
    setVizCalling(false);
    showToast('⏸ تم الإيقاف');
}

function scheduleNext(delayMs){
    clearTimeout(nextTimer);
    clearInterval(countdownTimer);
    if(delayMs>0){
        countdown=Math.ceil(delayMs/1000);
        document.getElementById('nextIn').textContent='التالي: '+countdown+'ث';
        countdownTimer=setInterval(function(){
            countdown--;
            if(countdown>0)document.getElementById('nextIn').textContent='التالي: '+countdown+'ث';
        },1000);
    }
    nextTimer=setTimeout(function(){callNextInQueue()},delayMs);
}

// ═══════ الاتصال الفعلي ═══════
async function callNextInQueue(){
    if(!isRunning)return;
    // تجاهل من تم الاتصال به
    while(currentIndex<contacts.length && contacts[currentIndex].status==='called'){
        currentIndex++;
    }
    if(currentIndex>=contacts.length){
        stopAutoCall();
        showToast('🎉 اكتملت جميع المكالمات');
        addToHistory({time:new Date().toISOString(),type:'complete',count:contacts.length});
        renderHistory();
        return;
    }

    const contact=contacts[currentIndex];
    document.getElementById('currentContact').textContent=contact.name+' • '+contact.number;
    document.getElementById('callStatus').textContent='⏳ جاري الاتصال...';
    showCallBanner(contact);

    let result;

    if(isLiveMode()){
        result=await makeRealCall(contact);
    }else{
        result=await simulateCall(contact);
    }

    if(result.ok){
        contact.status='called';
        contact.calledAt=new Date().toISOString();
        contact.failReason=null;
        showToast('✅ تم الاتصال بـ '+contact.name);
        addToHistory({time:contact.calledAt,type:'called',name:contact.name,number:contact.number,ok:true,duration:settings.callDuration});
        pulseViz();
        if(settings.soundAlert)playBeep(880);
    }else{
        contact.status='failed';
        contact.failReason=result.error||'فشل الاتصال';
        showToast('❌ فشل: '+contact.name+' — '+contact.failReason,true);
        addToHistory({time:new Date().toISOString(),type:'called',name:contact.name,number:contact.number,ok:false,error:contact.failReason});
        if(settings.soundAlert)playBeep(220);
        if(!settings.skipFailed){
            stopAutoCall();
            saveContacts(contacts);
            renderContacts();
            renderHistory();
            return;
        }
    }

    hideCallBanner();
    saveContacts(contacts);
    renderContacts();
    updateVizData(contacts);
    updateProgressUI();
    renderHistory();

    currentIndex++;
    saveQueue({currentIndex:currentIndex,running:true});

    if(isRunning)scheduleNext(settings.gapBetween*1000);
}

async function callNextNow(){
    if(!isRunning){toggleAutoCall();return}
    clearTimeout(nextTimer);
    clearInterval(countdownTimer);
    await callNextInQueue();
}

// ═══════ الاتصال الحقيقي عبر Cordova ═══════
function makeRealCall(contact){
    return new Promise(function(resolve){
        try{
            const plugin=window.cordova.plugins.CallNumber;
            // محاولة الاتصال المباشر (بدون لوحة الاتصال)
            plugin.callNumber(
                function(){ resolve({ok:true}) },
                function(err){ resolve({ok:false,error:String(err)}) },
                contact.number,
                true // bypassAppChooser: يتصل مباشرة
            );
            // بدء العد التنازلي لمدة المكالمة
            startCallDurationTimer(function(){
                // محاولة إنهاء المكالمة تلقائياً
                endCallIfPossible();
            });
        }catch(e){
            resolve({ok:false,error:'Cordova plugin error: '+e.message});
        }
    });
}

function startCallDurationTimer(onFinish){
    clearInterval(callTimer);
    callSeconds=0;
    updateCallTimerUI();
    callTimer=setInterval(function(){
        callSeconds++;
        updateCallTimerUI();
        if(callSeconds>=settings.callDuration){
            clearInterval(callTimer);
            if(onFinish)onFinish();
        }
    },1000);
}

function updateCallTimerUI(){
    const m=Math.floor(callSeconds/60);
    const s=callSeconds%60;
    const el=document.getElementById('callTimer');
    if(el)el.textContent=(m<10?'0':'')+m+':'+(s<10?'0':'')+s;
}

function endCallIfPossible(){
    // على Android 10+ يمكن إنهاء المكالمة عبر plugin
    // إن لم يتوفر، المستخدم يُنهي يدوياً
    try{
        if(window.cordova && window.cordova.plugins && window.cordova.plugins.PhoneCallTrap){}
        // ملاحظة: cordova-plugin-call-number لا يوفر endCall
        // الحل: المستخدم يُنهي المكالمة يدوياً أو بضغط زر
        document.getElementById('callStatus').textContent='⏱ انتهت المدة — أنهِ المكالمة';
        showToast('⏱ انتهت '+settings.callDuration+' ثوانٍ — أنهِ المكالمة');
    }catch(e){}
}

// ═══════ المحاكاة ═══════
function simulateCall(contact){
    return new Promise(function(resolve){
        startCallDurationTimer(function(){
            resolve({ok:true});
        });
    });
}

// ═══════ شريط المكالمة ═══════
function showCallBanner(contact){
    document.getElementById('callBanner').style.display='flex';
    document.getElementById('callName').textContent=contact.name;
    document.getElementById('callNumber').textContent=contact.number;
    callSeconds=0;
    updateCallTimerUI();
    setVizCalling(true);
}
function hideCallBanner(){
    document.getElementById('callBanner').style.display='none';
    setVizCalling(false);
}

// ═══════ واجهة ═══════
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
    c.innerHTML=filtered.map(function(ct){
        const idx=contacts.indexOf(ct);
        const isCurrent=idx===currentIndex&&isRunning;
        const cls=['contact-item',ct.status==='called'?'called':'',ct.status==='failed'?'failed':'',isCurrent?'active':''].filter(Boolean).join(' ');
        const statusLabel=ct.status==='called'?'✓ تم':ct.status==='failed'?'✗ فشل':'⏳ متبقي';
        return '<div class="'+cls+'" onclick="focusContact('+idx+')">'+
            '<div class="c-icon">'+(ct.status==='called'?'✅':ct.status==='failed'?'❌':'👤')+'</div>'+
            '<div class="c-info">'+
                '<div class="c-name">'+escapeHtml(ct.name)+'</div>'+
                '<div class="c-number">'+escapeHtml(ct.number)+'</div>'+
            '</div>'+
            '<button class="c-call" onclick="event.stopPropagation();manualCall('+idx+')"><i class="fas fa-phone"></i></button>'+
            '<span class="c-status '+ct.status+'">'+statusLabel+'</span>'+
        '</div>';
    }).join('');
}

function manualCall(idx){
    const ct=contacts[idx];
    if(!ct)return;
    if(isLiveMode()){
        makeRealCall(ct).then(function(r){
            if(r.ok)showToast('☎ جاري الاتصال بـ '+ct.name);
            else showToast('❌ فشل: '+r.error,true);
        });
    }else{
        // فتح الرابط tel: كحل بديل في المتصفح
        window.location.href='tel:'+ct.number;
    }
}

function focusContact(idx){
    const ct=contacts[idx];
    if(!ct)return;
    document.getElementById('currentContact').textContent=ct.name+' • '+ct.number;
    showToast('📌 '+ct.name);
}

function updateProgressUI(){
    const total=contacts.length;
    const called=contacts.filter(function(c){return c.status==='called'}).length;
    const failed=contacts.filter(function(c){return c.status==='failed'}).length;
    const pending=total-called-failed;
    document.getElementById('progressText').textContent=(called+failed)+' / '+total;
    document.getElementById('currentContact').textContent=total?(pending+' متبقي • '+called+' تم'):'لا يوجد';
}

function updateDuration(){
    const v=parseInt(document.getElementById('durationSlider').value);
    settings.callDuration=v;
    document.getElementById('durationValue').textContent=v+' ثوانٍ';
    saveSettings(settings);
}
function updateGap(){
    const v=parseInt(document.getElementById('gapSlider').value);
    settings.gapBetween=v;
    document.getElementById('gapValue').textContent=v+' ثوانٍ';
    saveSettings(settings);
}

function resetQueue(){
    if(!confirm('إعادة تعيين كل حالات الاتصال؟'))return;
    contacts.forEach(function(c){c.status='pending';c.calledAt=null;c.failReason=null});
    currentIndex=0;
    saveContacts(contacts);
    saveQueue({currentIndex:0,running:false});
    stopAutoCall();
    renderContacts();
    updateVizData(contacts);
    updateProgressUI();
    showToast('🔄 تم إعادة التعيين');
}

function exportData(){
    const data={exportedAt:new Date().toISOString(),duration:settings.callDuration,gap:settings.gapBetween,contacts:contacts,history:loadHistory()};
    const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
    const url=URL.createObjectURL(blob);
    const a=document.createElement('a');a.href=url;a.download='dialer_report_'+Date.now()+'.json';a.click();
    URL.revokeObjectURL(url);
    showToast('📥 تم التصدير');
}

function escapeHtml(s){return String(s).replace(/[&<>"']/g,function(m){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]})}
function playBeep(freq){try{const ctx=new (window.AudioContext||window.webkitAudioContext)();const o=ctx.createOscillator();const g=ctx.createGain();o.connect(g);g.connect(ctx.destination);o.frequency.value=freq;o.type='sine';g.gain.setValueAtTime(0.08,ctx.currentTime);g.gain.exponentialRampToValueAtTime(0.001,ctx.currentTime+0.15);o.start();o.stop(ctx.currentTime+0.15)}catch(e){}}

function loadContacts(){loadContactsFromFile()}"""

# ═══════════════════════════════════════════════════════════
# 📞 8. filters.js
# ═══════════════════════════════════════════════════════════

def build_filters_js():
    return """let currentFilters={type:'all',search:''};
function initFilters(){currentFilters=loadFilters();document.getElementById('searchBox').value=currentFilters.search||'';}
function toggleFilters(){const p=document.getElementById('filterPanel');p.style.display=p.style.display==='none'?'block':'none';document.getElementById('btnFilters').classList.toggle('active',p.style.display==='block')}
function setFilter(type,el){document.querySelectorAll('.filter-presets .preset-btn').forEach(function(b){b.classList.remove('active')});el.classList.add('active');currentFilters.type=type;saveFilters(currentFilters);renderContacts()}
function getFilteredContacts(){
    const q=(currentFilters.search||'').toLowerCase();
    return contacts.filter(function(c){
        if(q&&!(c.name.toLowerCase().indexOf(q)!==-1||c.number.toLowerCase().indexOf(q)!==-1))return false;
        switch(currentFilters.type){
            case 'pending':return c.status==='pending';
            case 'called':return c.status==='called';
            case 'failed':return c.status==='failed';
            default:return true;
        }
    });
}
document.addEventListener('input',function(e){
    if(e.target.id==='searchBox'){currentFilters.search=e.target.value;saveFilters(currentFilters);renderContacts()}
});"""

# ═══════════════════════════════════════════════════════════
# 📞 9. history.js
# ═══════════════════════════════════════════════════════════

def build_history_js():
    return """function toggleHistory(){const p=document.getElementById('historyPanel');p.style.display=p.style.display==='none'?'block':'none';document.getElementById('btnHistory').classList.toggle('active',p.style.display==='block');renderHistory()}
function renderHistory(){
    const c=document.getElementById('historyContent');
    const h=loadHistory();
    if(!h.length){c.innerHTML='<p class="history-line">📞 لا يوجد سجل بعد</p><p class="history-line">✨ ابدأ الاتصال لعرض السجل</p>';return}
    c.innerHTML=h.map(function(e,i){
        const t=new Date(e.time).toLocaleTimeString('ar');
        if(e.type==='load')return '<p class="history-line '+(i===0?'active':'')+'">📁 '+t+' — تم تحميل '+e.count+' جهة</p>';
        if(e.type==='complete')return '<p class="history-line '+(i===0?'active':'')+'">🎉 '+t+' — اكتملت المكالمات ('+e.count+')</p>';
        const cls=e.ok?'':'fail';
        return '<p class="history-line '+cls+' '+(i===0?'active':'')+'">'+(e.ok?'✅':'❌')+' '+t+' — '+escapeHtml(e.name)+' ('+escapeHtml(e.number)+')'+(e.duration?' - '+e.duration+'ث':'')+(e.error?' — '+escapeHtml(e.error):'')+'</p>';
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
    document.getElementById('openDialer').checked=settings.openDialer;
}
function saveSettings(){
    settings.skipFailed=document.getElementById('skipFailed').checked;
    settings.soundAlert=document.getElementById('soundAlert').checked;
    settings.simulate=document.getElementById('simulateMode').checked;
    settings.openDialer=document.getElementById('openDialer').checked;
    saveSettingsToStorage();
    showToast('⚙ تم الحفظ');
}
function saveSettingsToStorage(){saveData(KEYS.settings,settings)}"""

# ═══════════════════════════════════════════════════════════
# 📞 10. app.js
# ═══════════════════════════════════════════════════════════

def build_app_js():
    return """function showToast(msg,isError){
    const t=document.getElementById('toast');
    t.textContent=msg;
    t.classList.toggle('error',!!isError);
    t.classList.add('show');
    clearTimeout(t._timer);
    t._timer=setTimeout(function(){t.classList.remove('show')},2600);
}
(function boot(){
    initParticles();
    initVisualizer();
    initDialer();
    initFilters();

    // استرجاع الإعدادات
    const savedSettings=loadSettings();
    if(savedSettings.callDuration){
        document.getElementById('durationSlider').value=savedSettings.callDuration;
        document.getElementById('durationValue').textContent=savedSettings.callDuration+' ثوانٍ';
    }
    if(savedSettings.gapBetween){
        document.getElementById('gapSlider').value=savedSettings.gapBetween;
        document.getElementById('gapValue').textContent=savedSettings.gapBetween+' ثوانٍ';
    }

    // مؤشر الوضع
    setTimeout(function(){
        if(isCordova()){
            showToast('📱 تطبيق APK — اتصال حقيقي متاح');
        }else{
            showToast('🌐 متصفح — يُفتح تطبيق الاتصال عند التشغيل');
        }
    },800);

    console.log('%c📞 AUTO DIALER 2044 Ready','color:#00ff88;font-size:16px;font-weight:bold');

    // في Cordova: انتظر deviceready
    if(typeof window.cordova!=='undefined'){
        document.addEventListener('deviceready',function(){
            console.log('📞 Cordova ready');
            showToast('☎ صلاحيات الاتصال جاهزة');
        },false);
    }
})();"""

# ═══════════════════════════════════════════════════════════
# 📞 11. contacts.txt
# ═══════════════════════════════════════════════════════════

def build_contacts_txt():
    return """# AUTO DIALER 2044 - قائمة الأرقام
# الصيغة: رقم,اسم
# الأسطر التي تبدأ بـ # يتم تجاهلها

+9647712345678,أحمد محمد
+9647723456789,سارة علي
+9647734567890,خالد يوسف
+9647745678901,نورة عبدالله
+9647756789012,محمد العراقي
+9647767890123,فاطمة الزهراء
+9647778901234,عبدالرحمن
+9647789012345,ريم القحطاني
+9647790123456,سلطان الدوسري
+9647701234567,هند العتيبي
"""

# ═══════════════════════════════════════════════════════════
# 📞 12. config.xml (Cordova)
# ═══════════════════════════════════════════════════════════

def build_config_xml():
    return """<?xml version='1.0' encoding='utf-8'?>
<widget id="com.autodialer2044.app" version="1.0.0" xmlns="http://www.w3.org/ns/widgets" xmlns:cdv="http://cordova.apache.org/ns/1.0">
    <name>Auto Dialer 2044</name>
    <description>Sequential auto dialer for contacts list</description>
    <author email="you@example.com">Auto Dialer</author>
    <content src="index.html" />
    <access origin="*" />
    <allow-intent href="http://*/*" />
    <allow-intent href="https://*/*" />
    <allow-intent href="tel:*" />
    <allow-intent href="sms:*" />
    <preference name="DisallowOverscroll" value="true" />
    <preference name="android-minSdkVersion" value="22" />
    <preference name="android-targetSdkVersion" value="33" />
    <preference name="Orientation" value="portrait" />
    <preference name="Fullscreen" value="false" />
    <preference name="BackgroundColor" value="0xff050510" />
    <platform name="android">
        <edit-config file="app/src/main/AndroidManifest.xml" mode="merge" target="/manifest/application">
            <application android:usesCleartextTraffic="true" />
        </edit-config>
        <config-file target="AndroidManifest.xml" parent="/*">
            <uses-permission android:name="android.permission.CALL_PHONE" />
            <uses-permission android:name="android.permission.READ_PHONE_STATE" />
            <uses-permission android:name="android.permission.READ_CONTACTS" />
            <uses-permission android:name="android.permission.WRITE_CONTACTS" />
            <uses-permission android:name="android.permission.INTERNET" />
            <uses-permission android:name="android.permission.ANSWER_PHONE_CALLS" />
            <uses-permission android:name="android.permission.READ_PHONE_NUMBERS" />
        </config-file>
    </platform>
</widget>"""

# ═══════════════════════════════════════════════════════════
# 📞 13. package.json
# ═══════════════════════════════════════════════════════════

def build_package_json():
    return """{
  "name": "autodialer2044",
  "displayName": "Auto Dialer 2044",
  "version": "1.0.0",
  "description": "Sequential auto dialer app",
  "main": "index.js",
  "scripts": {
    "test": "echo no test"
  },
  "keywords": ["cordova", "dialer", "android"],
  "author": "Auto Dialer",
  "license": "MIT",
  "devDependencies": {
    "cordova-android": "^12.0.0",
    "cordova-plugin-call-number": "^1.5.0",
    "cordova-plugin-android-permissions": "^1.1.5"
  },
  "cordova": {
    "plugins": {
      "cordova-plugin-call-number": {},
      "cordova-plugin-android-permissions": {}
    },
    "platforms": ["android"]
  }
}"""

# ═══════════════════════════════════════════════════════════
# 📞 14. build.sh
# ═══════════════════════════════════════════════════════════

def build_build_sh():
    return """#!/bin/bash
# ═══════════════════════════════════════════════════════════
# AUTO DIALER 2044 - Build APK Script
# ═══════════════════════════════════════════════════════════
# المتطلبات: Node.js + Java JDK + Android SDK
# ═══════════════════════════════════════════════════════════

echo "📞 Building Auto Dialer 2044..."

# 1. تثبيت Cordova عالمياً
npm install -g cordova

# 2. إنشاء المشروع
cordova create AutoDialer com.autodialer2044.app "Auto Dialer 2044"
cd AutoDialer

# 3. حذف الملفات الافتراضية
rm -rf www/*

# 4. نسخ ملفاتنا
cp -r ../www/* www/
cp ../config.xml .
cp ../package.json .

# 5. إضافة منصة أندرويد
cordova platform add android

# 6. إضافة الإضافات المطلوبة
cordova plugin add cordova-plugin-call-number
cordova plugin add cordova-plugin-android-permissions

# 7. بناء APK
cordova build android --release

echo ""
echo "✅ تم بناء APK بنجاح!"
echo "📁 الملف: platforms/android/app/build/outputs/apk/release/"
"""

# ═══════════════════════════════════════════════════════════
# 📞 15. README.md
# ═══════════════════════════════════════════════════════════

def build_readme():
    return """# 📞 AUTO DIALER 2044

تطبيق أندرويد للاتصال التسلسلي التلقائي بقائمة أرقام من ملف TXT.

## ✨ المميزات
- 📁 قراءة جهات الاتصال من `contacts.txt`
- ⏱ تحديد مدة كل مكالمة (3-120 ثانية)
- ⏳ تحديد الفاصل بين المكالمات (1-30 ثانية)
- 🔄 اتصال تلقائي متسلسل
- 📊 متتبع تقدم (تم/متبقي/فشل)
- 📜 سجل كامل للاتصالات
- 🎨 تصميم Glass Morphism مستقبلي
- 💾 حفظ تلقائي للحالة
- 📥 تصدير تقرير JSON

## 🚀 التشغيل كموقع ويب
1. عدّل `contacts.txt`
2. ارفع الملفات على GitHub
3. افتح `index.html`
4. في المتصفح: يستخدم رابط `tel:` لفتح تطبيق الاتصال

## 📱 بناء APK حقيقي (اتصال عبر SIM)
### المتطلبات:
- Node.js
- Java JDK 17+
- Android SDK

### الخطوات:
```bash
chmod +x build.sh
./build.sh
