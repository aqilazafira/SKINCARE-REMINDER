document.addEventListener('DOMContentLoaded', function () {
    const generateBtn = document.getElementById('generate-btn');
    const scheduleDateInput = document.getElementById('schedule-date');
    const notification = document.getElementById('notification');
    const skinType = document.body.dataset.skinType;

    // Set default date to today
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0');
    const dd = String(today.getDate()).padStart(2, '0');
    scheduleDateInput.value = `${yyyy}-${mm}-${dd}`;

    generateBtn.addEventListener('click', generateRoutine);

    function showNotification(message, isError = false) {
        notification.textContent = message;
        notification.className = 'notification'; // Reset classes
        if (isError) {
            notification.classList.add('error');
        } else {
            notification.classList.add('success');
        }
        notification.style.display = 'block';

        setTimeout(() => {
            notification.style.display = 'none';
        }, 5000);
    }

    async function generateRoutine() {
        generateBtn.disabled = true;
        generateBtn.textContent = 'Generating...';
        showNotification('Scheduling your routine, please wait...', false);

        const selectedDate = scheduleDateInput.value;
        if (!selectedDate) {
            showNotification('Please select a date.', true);
            generateBtn.disabled = false;
            generateBtn.textContent = 'Generate My Routine';
            return;
        }

        // Get user's timezone
        const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

        const payload = {
            user_id: USER_ID, // This should be dynamically set in a real app
            date: selectedDate,
            user_timezone: userTimezone
        };

        try {
            const response = await fetch(`/rekomendasi/${skinType}/generate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || 'An unknown error occurred.');
            }

            showNotification(`Successfully created ${result.created_events.length} events in your calendar!`, false);

        } catch (error) {
            console.error('Error generating routine:', error);
            showNotification(`Error: ${error.message}`, true);
        } finally {
            generateBtn.disabled = false;
            generateBtn.textContent = 'Generate My Routine';
        }
    }
});
