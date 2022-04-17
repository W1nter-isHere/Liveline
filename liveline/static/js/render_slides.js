let view = $("#pres-view");

let pres;
let isHost;
let isEditable;

let votes;

let currentSlide = 0;
let slideCount;

function reloadSlidesEditable(room, editable) {
    isHost = !room;
    isEditable = editable;

    if (room) {
        pres = JSON.parse(httpGet(`/viewer/${ROOM_CODE}.json`)).slides;
    } else {
        pres = JSON.parse(httpGet(`/viewer/id/${ID}.json`)).slides;
    }

    if (pres == undefined) return;

    slideCount = pres.length
    if (currentSlide >= pres.length || currentSlide < 0) {
        currentSlide = 0;
    }

    if (slideCount > 0) {
        renderSlide(currentSlide);
    } else {
        view.empty();
    }

    updateIndexLabel();
}

function renderSlides(room) {
    reloadSlidesEditable(room, false)
}

function renderSlide(idx) {
    view.empty();

    slide = pres[idx];

    view.append(
        $("<h1></h1>", {
            contenteditable: isEditable,
            class: "slide_editable"
        }).text(slide.title)
    );

    switch(slide.typ) {
        case "TitleSlide":
            titleSlide(slide);
            break;
        case "TextSlide":
            textSlide(slide);
            break;
        case "ImageSlide":
            imageSlide(slide);
            break;
        case "PollSlide":
            pollSlide(slide);
            break;
    }
}

function setClass(id) {
    view.attr("class", id);
}

function titleSlide(slide) {
    setClass('title-slide')

    let content = $("<article></article>")
    view.append(content)

    if(slide.image !== null) {
        content.append(
            $("<img />", {
                src: slide.image,
                class: "slide_img_editable"
            })
        );
    }
}

function textSlide(slide) {
    setClass('text-slide')

    let content = $("<article></article>")
    view.append(content)

    let text = $("<p></p>", {
        contenteditable: isEditable,
        class: "slide_editable"
    }).text(slide.text)

    content.append(
        // $("<div></div>").append(
            text
        // )
    );

    // let startSize = 3

    // console.log(text("#text").height())
    // console.log(content.height())

    // if ($('#div-id')[0].scrollWidth >  $('#div-id').innerWidth()) {
    //     //Text has over-flown
    // }

    // while(text.height() > content.height()) {
    //     startSize -= 0.1
    //     text.css("font-size", `${startSize}vh`)
    // }

    if(slide.image !== null) {
        content.append(
            $("<img />", {
                src: slide.image,
                class: "slide_img_editable"
            })
        );
    }
}

function imageSlide(slide) {
    setClass('image-slide')

    let content = $("<article></article>")
    view.append(content)

    const imageCount = slide.images.length; 

    if(imageCount > 0) {
        for (let i = 0; i < imageCount; i++) {
            content.append(
                $("<div></div>", {
                    class: "img-container"
                }).append(
                    $("<img />", {
                        src: slide.images[i],
                        class: "slide_img_editable"
                    })
                )
            );
        }
    }

    
}

function pollSlide(slide) {
    setClass('poll-slide')

    let content = $("<article></article>")
    view.append(content)

    if(slide.image !== null) {
        content.append(
            $("<img />", {
                src: slide.image,
                class: "slide_img_editable"
            })
        );
    }

    optionContainer = $("<div></div>");
    content.append(optionContainer);

    if(isHost) {
        slide.options.forEach(element => {
            optionContainer.append(
                $("<div></div>").append(
                    $("<p></p>").text(0)
                ).append(
                    $("<p></p>").text(element)
                )
            )
        });
    } else {
        slide.options.forEach((element, idx) => {
            optionContainer.append(
                $("<button></button>", {
                    class: "hoverable button",
                    onclick: voteButton(idx)
                }).text(element)
            )
        });
    }
}

function getTextHeight(text) {
    parseInt(window.getComputedStyle(text[0]).fontSize, 10);
}

function nextSlideLocal() {
    if (currentSlide + 1 < slideCount) {
        incrementCurrentSlide();
        renderSlide(currentSlide);
    }
}

function lastSlideLocal() {
    if (currentSlide - 1 >= 0) {
        decrementCurrentSlide();
        renderSlide(currentSlide);
    }
}

function incrementCurrentSlide() {
    currentSlide++;
    updateIndexLabel();
}

function decrementCurrentSlide() {
    currentSlide--;
    updateIndexLabel();
}

function updateIndexLabel() {
    const indexLabel = $("#slide_index");
    if (indexLabel != null && indexLabel != undefined) {
        indexLabel.text(currentSlide + 1);
    }
}

function saveSlides() {
    
}