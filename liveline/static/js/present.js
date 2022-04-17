const socket = io();
let hostKey;
let roomCode;



// client-side
socket.on("connect", () => {
    console.log(socket.id); // x8WIv7-mJelg7on_ALbx
});

socket.on("join", (data) => {
    console.log(data); // x8WIv7-mJelg7on_ALbx
});

socket.on("newRoom", (data) => {
    hostKey = data.host_key;
    roomCode = data.code;
    console.log(hostKey);
    console.log(roomCode);
});

socket.on("castVote", (data) => {
    votes[data.slide]
});

function present() {
    socket.emit("newRoom", {
        ID: ID
    });
}

function endPresent() {
    socket.emit("endPresentation");
}

function updateSlide() {
    renderSlide(currentSlide)
    socket.emit("changeSlide", {
        room: roomCode,
        slide: currentSlide
    });
}

function nextSlide() {
    if (currentSlide + 1 < slideCount) {
        incrementCurrentSlide();
        updateSlide();
    }
}

function lastSlide() {
    if (currentSlide - 1 >= 0) {
        decrementCurrentSlide();
        updateSlide();
    }
}

function pingServer() {
    socket.emit("pingRoom", {
        room: roomCode,
        hostKey: hostKey
    });
}

setInterval(pingServer, 29000)