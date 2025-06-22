document.addEventListener('DOMContentLoaded', function() {
    const carousel = document.getElementById('profilePicCarousel');
    const items = carousel.querySelectorAll('.carousel-item');
    const hiddenInput = document.getElementById('profile_pic');

    function selectItem(idx) {
        items.forEach((item, i) => {
            if (i === idx) {
                item.classList.add('selected');
                hiddenInput.value = item.getAttribute('data-pic');
            } else {
                item.classList.remove('selected');
            }
        });
    }

    // Click on image to select
    items.forEach((item, idx) => {
        item.querySelector('img').addEventListener('click', function() {
            selectItem(idx);
            // Move carousel to this item
            const carouselInstance = bootstrap.Carousel.getOrCreateInstance(carousel);
            carouselInstance.to(idx);
        });
    });

    // Update selection on slide
    carousel.addEventListener('slid.bs.carousel', function(e) {
        selectItem(e.to);
    });

    // Set initial selection
    selectItem(0);
});
