/**
 * homeThumbs.js
 * 
 * Manages the sizing and dynamic loading of thumbnail carousels on the home page.
 * Thumbnails are loaded as batches for a nice scrolling experience.
 * The number of thumbnails per batch is determined by the screen width.
 * The width of each thumbnail is adjusted based on the parent container's width.
 */


/**
 * Dynamically updates the thumbnail carousels based on screen size and parent container width.
 * It calculates the appropriate batch size and thumbnail width, then applies these styles to the thumbnails.
 */
document.addEventListener('DOMContentLoaded', () => {
    const updateCarousels = () => {
        // Get the screen width
        const screenWidth = window.innerWidth;

        // Get the width of the parent div (which is narrower than the screen width)
        const parentDiv = document.querySelector('#continueWatchingCarousel');
        const parentWidth = parentDiv ? parentDiv.offsetWidth : screenWidth;
                    
        // Padding makes the thumbnails fit nicely within the parent container
        // Default padding is 35px
        let padding = 35;

        // Determine batch size and tune padding based on screen width
        if (screenWidth <= 400) {
            batchSize = 2;
            padding = 17;
        } else if (screenWidth <= 576) {
            batchSize = 2;
            padding = 20;
        } else if (screenWidth <= 820) {
            batchSize = 3;
        } else if (screenWidth <= 1024) {
            batchSize = 3;
        } else {
            batchSize = 3;
        }

        // Determine the thumbnail width
        let thumbnailWidth = (parentWidth - padding) / batchSize;
        if (thumbnailWidth > 330) {
            // Maximum thumbnail width is 330px
            thumbnailWidth = 330;
        }
        
        // Apply the width to all .thumbnail-home elements
        const thumbnails = document.querySelectorAll('.thumbnail-home');
        thumbnails.forEach(thumbnail => {
            thumbnail.style.width = `${thumbnailWidth}px`;
        });

        // Select all carousels on the page
        const carousels = document.querySelectorAll('.carousel[data-dynamic="true"]');
        carousels.forEach(carousel => {
            const carouselInner = carousel.querySelector('.carousel-inner');
            const videos = Array.from(carouselInner.querySelectorAll('.thumbnail-home'));
            carouselInner.innerHTML = ''; // Clear existing items

            // Create batches
            for (let i = 0; i < videos.length; i += batchSize) {
                const batch = videos.slice(i, i + batchSize);
                const carouselItem = document.createElement('div');
                carouselItem.classList.add('carousel-item');
                if (i === 0) carouselItem.classList.add('active'); // First batch is active

                const batchContainer = document.createElement('div');
                batchContainer.classList.add('d-flex', 'gap-3', 'justify-content-center');
                batch.forEach(video => batchContainer.appendChild(video));

                carouselItem.appendChild(batchContainer);
                carouselInner.appendChild(carouselItem);
            }

            // Make the carousel visible after adjustment
            carousel.style.visibility = 'visible';
            carousel.style.opacity = '1';
        });
    };

    // Run on page load and on window resize
    updateCarousels();
    window.addEventListener('resize', updateCarousels);
});
