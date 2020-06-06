var video = document.querySelector('video');
var start_btn = document.getElementById('btn-start-recording')
var stop_btn = document.getElementById('btn-stop-recording')
var upload_btn = document.getElementById('btn-upload-recording')
var link = document.getElementById('filename')
var file = null;
var recorder; // globally accessible
const upload_url = `/screen`
// not start is disabled
stop_btn.disabled = true
upload_btn.disabled = true

// check 
if (!navigator.getDisplayMedia && !navigator.mediaDevices.getDisplayMedia) {
    var error = 'Your browser does NOT support the getDisplayMedia API.';
    document.querySelector('h1').innerHTML = error;
    video.style.display = 'none';
    start_btn.style.display = 'none';
    stop_btn.style.display = 'none';
    upload_btn.style.display = 'none';
    throw new Error(error);
}

function invokeGetDisplayMedia(success, error) {
    var displaymediastreamconstraints = {
        video: {
            displaySurface: 'monitor', // monitor, window, application, browser
            logicalSurface: true,
            cursor: 'always' // never, always, motion
        }
    };

    // above constraints are NOT supported YET
    // that's why overridnig them
    displaymediastreamconstraints = {
        video: true
    };

    if (navigator.mediaDevices.getDisplayMedia) {
        navigator.mediaDevices.getDisplayMedia(displaymediastreamconstraints).then(success).catch(error);
    } else {
        navigator.getDisplayMedia(displaymediastreamconstraints).then(success).catch(error);
    }
}

function captureScreen(callback) {
    invokeGetDisplayMedia(function (screen) {
        addStreamStopListener(screen, function () {
            stop_btn.click();
        });
        callback(screen);
    }, function (error) {
        console.error(error);
        alert('Unable to capture your screen. Please check console logs.\n' + error);
    });
}

function stopRecordingCallback() {
    video.src = video.srcObject = null;
    file = recorder.getBlob()
    video.src = URL.createObjectURL(file);
    console.log(video)
    recorder.screen.stop();
    recorder.destroy();
    recorder = null;
    start_btn.disabled = false;
    upload_btn.disabled = false;
}

function addStreamStopListener(stream, callback) {
    stream.addEventListener('ended', function () {
        callback();
        callback = function () {};
    }, false);
    stream.addEventListener('inactive', function () {
        callback();
        callback = function () {};
    }, false);
    stream.getTracks().forEach(function (track) {
        track.addEventListener('ended', function () {
            callback();
            callback = function () {};
        }, false);
        track.addEventListener('inactive', function () {
            callback();
            callback = function () {};
        }, false);
    });
}

// onclick 
// start btn
start_btn.onclick = function () {
    this.disabled = true;
    file = null;
    captureScreen(function (screen) {
        video.srcObject = screen;

        recorder = RecordRTC(screen, {
            type: 'video'
        });

        recorder.startRecording();

        // release screen on stopRecording
        recorder.screen = screen;

        stop_btn.disabled = false;
        upload_btn.disabled = true;
    });
};

// stop btn
stop_btn.onclick = function () {
    this.disabled = true;
    recorder.stopRecording(stopRecordingCallback);
};

// upload
upload_btn.onclick = function () {
    this.disabled = true;
    if(!recorder && file){
        // blob to file
        let formData = new FormData()
        let upload_file = new File([file],`v_${guid()}.${file.type.split('/')[1]}`,{ type: file.type })
        formData.append("file",upload_file)
        console.log(upload_file)
        // do upload
        fetch(upload_url, {
            method: 'POST',
            body: formData,
        }).then(resp => resp.json()).then(resp => {
            console.log(resp)
            alert(resp['message'])
            link.href = resp['data']
            link.innerHTML = `解帧`
            console.log(link)
        }).catch(error => console.error('Error:', error))
    }
};


function guid() {
    function S4() {
        return (((1+Math.random())*0x10000)|0).toString(16).substring(1);
    }
    return (S4()+S4()+"-"+S4()+"-"+S4()+"-"+S4()+"-"+S4()+S4()+S4());
}


