function viewVote() {
    var voteStarView = document.getElementById("voteProfile");
    var btnVote = document.getElementsByClassName("rated")[0];
    if (voteStarView.style.display === "none") {
        voteStarView.style.display = "flex";
        btnVote.style.display = "none";
    } else {
        voteStarView.style.display = "none";
        btnVote.style.display = "flex";
    }
}