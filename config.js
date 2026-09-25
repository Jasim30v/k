// SMS BLASTER 2044 - Configuration
const CONFIG = {
    twilio: {
        accountSid: '',
        authToken: '',
        fromNumber: '',
        endpoint: 'https://api.twilio.com/2010-04-01/Accounts'
    },
    backend: {
        enabled: false,
        url: 'https://your-worker.workers.dev/send',
        apiKey: ''
    },
    defaults: {
        intervalSeconds: 30,
        contactsFile: 'contacts.txt',
        senderId: 'Company',
        simulate: true,
        soundAlert: true,
        skipFailed: false
    },
    limits: {
        minInterval: 5,
        maxInterval: 300,
        maxHistoryEntries: 200,
        smsLength: 160
    }
};

function isLiveMode(){
    return !CONFIG.defaults.simulate && (
        (CONFIG.twilio.accountSid && CONFIG.twilio.authToken && CONFIG.twilio.fromNumber) ||
        CONFIG.backend.enabled
    );
}