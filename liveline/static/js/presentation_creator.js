function deleteSlide() {
    httpGetAsync("/host/presentation_creator/${ID}/delete_slide/${currentSlide}", resp => {
        reloadSlides();
    });
}