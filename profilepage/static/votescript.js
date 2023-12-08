// Hiển thị bảng tùy chọn vote
function viewVote() {
    var voteStarView = document.getElementById("voteProfile");
    var btnVote = document.getElementById("buttonvote");
    if (voteStarView.style.display === "none") {
        voteStarView.style.display = "flex";
        btnVote.style.display = "none";
    } else {
        voteStarView.style.display = "none";
        btnVote.style.display = "flex";
    }
}
