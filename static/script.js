document.addEventListener('DOMContentLoaded', () => {
    // Smooth scrolling for navigation links
    const navLinks = document.querySelectorAll('nav a');

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');

            // Agar link #se start hota hai (same page section) tabhi scroll kare
            if (href.startsWith("#")) {
                e.preventDefault();
                const targetId = href.substring(1);
                const targetSection = document.getElementById(targetId);

                if (targetSection) {
                    window.scrollTo({
                        top: targetSection.offsetTop - 80, // Adjust for fixed header
                        behavior: 'smooth'
                    });
                }
            }
            // warna (jaise /products) normal redirect hone do
        });
    });
});
