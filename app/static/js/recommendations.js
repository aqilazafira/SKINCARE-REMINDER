document.addEventListener('DOMContentLoaded', function () {
    const generateBtn = document.getElementById('generate-btn');
    const notification = document.getElementById('notification');
    
    // Modal elements
    const completionModal = document.getElementById('completion-modal');
    const completionMessage = document.getElementById('completion-message');
    const closeModalBtn = document.getElementById('close-modal-btn');
    const skinType = document.body.dataset.skinType;
    const storageKey = `skincareState_${skinType}`;

    // Load saved state from Local Storage when page loads
    loadState();

    generateBtn.addEventListener('click', handleRoutineCompletion);
    
    if(closeModalBtn) {
        closeModalBtn.addEventListener('click', () => {
            completionModal.style.display = 'none';
        });
    }

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

    function handleRoutineCompletion() {
        const morningCheckboxes = document.querySelectorAll('#morning-steps input[type="checkbox"]');
        const nightCheckboxes = document.querySelectorAll('#night-steps input[type="checkbox"]');

        const checkedMorning = document.querySelectorAll('#morning-steps input:checked').length;
        const checkedNight = document.querySelectorAll('#night-steps input:checked').length;

        const totalMorning = morningCheckboxes.length;
        const totalNight = nightCheckboxes.length;

        let message = '';
        const isMorningComplete = (totalMorning > 0) && (checkedMorning === totalMorning);
        const isNightComplete = (totalNight > 0) && (checkedNight === totalNight);
        const anyChecked = (checkedMorning > 0) || (checkedNight > 0);

        if (isMorningComplete && isNightComplete) {
            message = "Self-care completed! Pilihan terbaik yang kamu ambil hari ini adalah merawat diri.";
        } else if (isMorningComplete && checkedNight === 0) {
            message = "Kulitmu semakin siap menghadapi hari! Hebat, kamu sudah merawat dirimu dengan baik";
        } else if (isNightComplete && checkedMorning === 0) {
            message = "Kerja keras seharian layak ditutup dengan perawatan. Kulitmu berterima kasih!";
        } else if (anyChecked) { // This covers all partial completion cases
            message = "Ambil napas sebentar, lalu lanjutkan. Kamu sudah melangkah dengan baik.";
        } else {
            showNotification('Pilih setidaknya satu langkah rutinitas.', true);
            return;
        }

        // Display the modal
        if(completionModal && completionMessage) {
            completionMessage.textContent = message;
            completionModal.style.display = 'flex';
        }

        // Save the current state of checkboxes to Local Storage
        saveState();
    }

    function saveState() {
        const checkedIds = [];
        document.querySelectorAll('.routine-container input:checked').forEach(cb => {
            checkedIds.push(cb.id);
        });
        localStorage.setItem(storageKey, JSON.stringify(checkedIds));
    }

    function loadState() {
        const savedState = localStorage.getItem(storageKey);
        if (savedState) {
            const checkedIds = JSON.parse(savedState);
            checkedIds.forEach(id => {
                const checkbox = document.getElementById(id);
                if (checkbox) {
                    checkbox.checked = true;
                }
            });
        }
    }
});
