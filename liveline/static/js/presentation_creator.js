const socket = io();

function deleteSlide() {
    httpGetAsync(`/host/presentation_creator/${ID}/delete_slide/${currentSlide}`, resp => {
        save();
        reloadSlidesEditable(false, true);
    });
}

function addNewSlide(type) {
    httpGetAsync(`/host/presentation_creator/${ID}/add_slide/${type}`, resp => {
        save();
        reloadSlidesEditable(false, true);
    });
}

function save() {
    let texts = document.querySelectorAll(".slide_editable");
    let images = document.querySelectorAll(".slide_img_editable");

    let textList = [];
    let imageList = [];

    for(let i = 0; i < texts.length; i++) {
        textList.push(texts[i].innerHTML);
    }

    for(let i = 0; i < images.length; i++) {
        imageList.push(images[i].getAttribute("src"));
    }

    socket.emit("save", {
        index: currentSlide,
        presentationID: ID,
        texts: textList,
        images: imageList
    })
}

document.addEventListener("click", (event) => {
    const contextMenu = document.querySelector("#context-menu");
    if (event.target.offsetParent != contextMenu) {
        contextMenu.style.display = "none";
        contextMenu.removeAttribute("pres-selected");
    }
});

function setRenameData() {
    const contextMenu = document.querySelector("#context-menu");
    const presentationid = contextMenu.getAttribute("pres-selected");
    const form = document.querySelector("#rename_setup");
    const input = document.createElement("input");
    input.setAttribute("hidden", "hidden");
    input.setAttribute("type", "text");
    input.setAttribute("name", "pres_id");
    input.setAttribute("id", "pres_id");
    input.setAttribute("value", `${presentationid}`)
    form.appendChild(input);
}