document.addEventListener('DOMContentLoaded', function () {

    const modal = document.getElementById('gameModal');
    const closeBtn = document.querySelector('.close');

    document.querySelectorAll('.view-details-btn').forEach(button => {
        button.addEventListener('click', () => {
            const game = JSON.parse(button.dataset.game);
            document.getElementById('modalTitle').innerText = game.title;
            document.getElementById('modalType').innerText = game.game_type || 'None';
            document.getElementById('modalDescription').innerText = game.description || 'No description';
            document.getElementById('modalMaxPlayers').innerText = game.max_players;
            document.getElementById('modalCreatedBy').innerText = game.created_by;
            modal.style.display = 'block';
        });
    });

    closeBtn.onclick = () => modal.style.display = 'none';
    window.onclick = e => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    };

    // Filters
    const filterCheckboxes = document.querySelectorAll('.filter-checkbox input');

    filterCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function () {
            const selectedTypes = Array.from(filterCheckboxes)
                .filter(cb => cb.checked)
                .map(cb => cb.value);

            const gameCards = document.querySelectorAll('.game-card');

            gameCards.forEach(card => {
                const cardType = card.dataset.type;
                const shouldShow = selectedTypes.length === 0 || selectedTypes.includes(cardType);
                card.style.display = shouldShow ? 'flex' : 'none';
            });
        });
    });
});