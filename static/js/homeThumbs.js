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
    // Check if the device is a TV or large screen
    const isTV = window.tvDetection.isTV();
    
    // Apply specific styles and behaviors for TV or large screens
    if (isTV) {
        // Larger thumbnails and fewer per row for TV
        const updateCarouselsForTV = () => {
            const screenWidth = window.innerWidth;
            let batchSize = 4; // Fewer items per row on TV
            let thumbnailWidth = 320; // Larger thumbnails
            
            if (screenWidth >= 3840) { // 4K TVs
                batchSize = 6;
                thumbnailWidth = 350;
            }
            
            const thumbnails = document.querySelectorAll('.thumbnail-home');
            thumbnails.forEach(thumbnail => {
                thumbnail.style.width = `${thumbnailWidth}px`;
                thumbnail.style.height = `${thumbnailWidth * 0.75}px`; // Maintain aspect ratio
            });
            
            // Auto-advance carousel every 10 seconds
            const carousels = document.querySelectorAll('.carousel[data-dynamic="true"]');
            carousels.forEach(carousel => {
                setInterval(() => {
                    const nextButton = carousel.querySelector('.carousel-control-next');
                    if (nextButton && !document.querySelector('.tv-focused')) {
                        nextButton.click();
                    }
                }, 10000);
            });
        };
        
        updateCarouselsForTV();

        // Listen for TV mode changes
        window.addEventListener('tvModeChanged', (e) => {
            if (e.detail.isTV) {
                updateCarouselsForTV();
            } else {
                // Reset to normal carousel behavior
                location.reload(); // Simple approach to reset
            }
        });
    }


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

        // Select all carousels on the page
        const carousels = document.querySelectorAll('.carousel[data-dynamic="true"]');
        carousels.forEach(carousel => {
            const carouselInner = carousel.querySelector('.carousel-inner');
            const videos = Array.from(carouselInner.querySelectorAll('.thumbnail-home'));
            carouselInner.innerHTML = ''; // Clear existing items

            // Use the width of the current carousel
            const parentWidth = carousel.offsetWidth || window.innerWidth;

            // Determine the thumbnail width
            let thumbnailWidth = (parentWidth - padding) / batchSize;
            if (thumbnailWidth > 330) {
                // Maximum thumbnail width is 330px
                thumbnailWidth = 330;
            }
            
            // Apply the width to all .thumbnail-home elements
            videos.forEach(thumbnail => {
                thumbnail.style.width = `${thumbnailWidth}px`;
            });

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
