const chatbotIcon = document.getElementById('chatbotIcon');
      const drawer = document.getElementById('drawer');

      // Function to toggle the drawer
      function toggleDrawer() {
        drawer.classList.toggle('translate-x-full');
      }

      // Open the drawer when the chatbot icon is clicked
      chatbotIcon.addEventListener('click', (event) => {
        event.stopPropagation(); // Prevent the click from bubbling up to the document
        toggleDrawer();
      });

      // Close the drawer when clicking outside of it
      document.addEventListener('click', (event) => {
        if (!drawer.classList.contains('translate-x-full') && !chatbotIcon.contains(event.target)) {
          toggleDrawer();
        }
      });