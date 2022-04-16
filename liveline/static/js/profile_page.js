const label = document.querySelector("#no-presentation-label");

if (label != null && label != undefined) {
    const presentationData = JSON.parse(httpGet("/profile/user/presentations"));
    console.log(presentationData);
    const presentationCount = presentationData.length

    // if there is presentation(s)
    if (presentationCount > 0) {
        label.setAttribute("hidden", "hidden");
    
        for (let i = 0; i < presentationCount; i++) {
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
            presentationElement.innerHTML = presentation.name;
            groupContent.appendChild(presentationElement);
        }
    }
}