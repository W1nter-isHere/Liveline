const label = document.querySelector("#no-presentation-label");

if (label != null && label != undefined) {
    const presentationData = JSON.parse(httpGet("/profile/user/presentations"));
    const presentationCount = presentationData.length

    // if there is presentation(s)
    if (presentationCount > 0) {
        label.setAttribute("hidden", "hidden");
        
        for (let i = 0; i < presentationCount; i++) {
            if (presentationData[i] == undefined) continue;
            makePresentationPreviewElement(presentationData[i])
        }
    }

    // show label if there is no prsentation
    if (presentationCount <= 0) {
        label.removeAttribute("hidden");
    }
}

function makePresentationPreviewElement(presentation) {
    const group = document.querySelector("#presentations");
    if (group != null && group != undefined) {
        const groupContent = group.getElementsByClassName("section-content")[0];
        if (groupContent != null && groupContent != undefined) {
            const presentationElement = document.createElement("a");
            presentationElement.setAttribute("class", "presentation-preview hoverable");
            presentationElement.setAttribute("href", "/host/present/"+presentation.identifier);
            presentationElement.addEventListener("contextmenu", (event) => {
                event.preventDefault();
                const contextMenu = document.querySelector("#context-menu");
                contextMenu.setAttribute("pres-selected", `${presentation.identifier}`);
                contextMenu.style.display = "flex";
                contextMenu.style.position = "absolute";
                contextMenu.style.top = `${window.event.clientY}px`;
                contextMenu.style.left = `${window.event.clientX}px`;
            });
            presentationElement.innerHTML = presentation.name;
            groupContent.appendChild(presentationElement);
        }
    }
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

function deletePres() {
    const contextMenu = document.querySelector("#context-menu");
    const presentationid = contextMenu.getAttribute("pres-selected");
    httpGet(`/profile/user/delete_pres/${presentationid}`)
    window.location.reload()
}