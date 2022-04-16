
// request data
let jsonData = JSON.parse(httpGet("/viewer/widget_based/{{id}}/slide"));
console.log("Received slide data");

// get main group
const mainGroup = document.querySelector("#slideshow-view");

// create background element
const bg = document.createElement("img");
bg.setAttribute("src", jsonData.background);
bg.setAttribute("alt", "background");
bg.style.width = "100%";
bg.style.height = "100%";
bg.style.zIndex = "-10";
mainGroup.appendChild(bg)

// get widgets
const widgets = jsonData.widgets;

// setup widgets
for (let i = 0; i < widgets.length; i++) {
    const widget = widgets[i];

    switch (widget.widget_type) {
        case 0:
            const textElement = document.createElement("p");
            console.log(widget.content);
            mainGroup.appendChild(textElement);
            textElement.innerHTML = widget.content;
            setupWidgetPosition(textElement, widget);
            break;
        case 1:
            const imgElement = document.createElement("img");
            mainGroup.appendChild(imgElement);
            imgElement.setAttribute("src", widget.content);
            imgElement.setAttribute("alt", widget.content);
            setupWidgetPosition(textElement, widget);
            break;
    }
}

function setupWidgetPosition(element, widget)
{   
    element.style.position = "absolute";
    element.style.left = widget.position[0] + "px";
    element.style.top = widget.position[1] + "px";
}