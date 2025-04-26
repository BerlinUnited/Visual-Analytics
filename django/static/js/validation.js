function handle_validation(){
    const button = document.getElementById('validate_button');
    const left_container = document.getElementById('left');
    let isActive = false;
    
    button.addEventListener('click', async () => {
        // Toggle state
        isActive = !isActive;
        // Update button appearance
        if (isActive) {
            button.classList.add('active');
            button.innerText = 'Validated';
            left_container.style.boxShadow = "inset 2px 2px 108px -38px rgba(52, 243, 4),inset -2px -2px 108px -38px rgba(52, 243, 4)";
        } else {
            button.classList.remove('active');
            button.innerText = 'Validate';
            left_container.style.boxShadow = "";
        }
    });
}