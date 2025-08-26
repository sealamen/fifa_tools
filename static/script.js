document.addEventListener("DOMContentLoaded", function() {
    const modal = document.getElementById("modal");
    const modalBody = document.getElementById("modal-body");
    const modalClose = document.getElementById("modal-close");

    // 모달 닫기
    modalClose.onclick = function() {
        modal.style.display = "none";
        modalBody.innerHTML = "";
    }

    // 테이블 행 클릭 이벤트
    document.querySelectorAll(".match-row").forEach(row => {
        row.addEventListener("click", async () => {
            const matchId = row.dataset.matchId;
            const response = await fetch(`/api/match/${matchId}`);
            const data = await response.text(); // HTML fragment 반환

            modalBody.innerHTML = data;
            modal.style.display = "block";
        });
    });
});
