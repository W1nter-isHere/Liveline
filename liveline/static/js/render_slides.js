let pres;

let currentSlide = 0;
let slideCount;

let view = $("#pres-view");

function reloadSlides(room) {
    if (room) {
        pres = JSON.parse(httpGet(`/viewer/${ROOM_CODE}.json`)).slides;
    } else {
        pres = JSON.parse(httpGet(`/viewer/id/${ID}.json`)).slides;
    }

    slideCount = pres.length
    if (currentSlide >= pres.length || currentSlide < 0) {
        currentSlide = 0;
    }
    renderSlide(currentSlide);
}

function renderSlide(idx) {
    view.empty();

    slide = pres[idx]

    view.append(
        $("<h1></h1>").text(slide.title)
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
                src: slide.image
            })
        );
    }
}

function textSlide(slide) {
    setClass('text-slide')

    let content = $("<article></article>")
    view.append(content)

    let text = $("<p></p>").text(slide.text)

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
                src: slide.image
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
                        src: slide.images[i]
                    })
                )
            );
        }
    }
}

function getTextHeight(text) {
    parseInt(window.getComputedStyle(text[0]).fontSize, 10);
}

function nextSlideLocal() {
    if (currentSlide + 1 < slideCount) {
        currentSlide++;
        renderSlide(currentSlide);
    }
}

function lastSlideLocal() {
    if (currentSlide - 1 >= 0) {
        currentSlide--;
        renderSlide(currentSlide);
    }
}