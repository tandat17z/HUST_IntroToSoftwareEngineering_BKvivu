        function likeAction(event, postId) {
            const button = event.currentTarget;
            const likeElement = document.getElementById(postId + "_like");
            const like = parseInt(likeElement.innerText, 10);
            let newLike = like;
            if( button.value === "false"){
                newLike = like + 1;
                button.value = "true";
                button.style.backgroundColor = '#f00';
            }
            else{
                newLike = like - 1;
                button.value = "false";
                button.style.backgroundColor = '#fff';
            }
            likeElement.innerText = newLike

            // Gửi yêu cầu AJAX để cập nhật số lượng like trên server
            const xhr = new XMLHttpRequest();
            xhr.open("POST", `/postspage/update_likes/${postId}/`, true);
            xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
            xhr.send(JSON.stringify({ like: newLike}));
        }
    function insertComment(event, postId){
        const inputCmt = document.getElementById(postId + "_comment");
        const contentCmd = inputCmt.value;
        inputCmt.value = '';
        // Gửi yêu cầu AJAX để cập nhật số lượng like trên server
        const xhr = new XMLHttpRequest();
        xhr.open("POST", `/postspage/insert_comment/${postId}/`, true);
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhr.send(JSON.stringify({comment: contentCmd}));
        alert("Comment thành công rồi nhé");

        // Tăng _commentNum
        const cmtNum = document.getElementById(postId + "_commentNum");
        cmtNum.innerText = parseInt(cmtNum.innerText, 10) + 1
        showCmt(postId)
    }
    function showComment(event, postId){
        showCmt(postId)
    }
    function showCmt(postId) {
        // Ngăn chặn hành động mặc định của nút  event.preventDefault();
        const cmtElm = document.getElementById("containerComment");
        console.log("ấn show comment rồi")
        cmtElm.style.display = "flex";
        // Gửi yêu cầu AJAX để lấy dữ liệu comment
        $.ajax({
            url: `/postspage/get_comments/${postId}/`,
            method: 'GET',
            success: function(response) {
                // Xử lý dữ liệu JSON nhận được
                var comments = response.comments;
                var containerComment = document.getElementById('allCommentOfPostId');

                // Xóa nội dung cũ trong containerComment
                containerComment.innerHTML = '';

                // Thêm các comment mới vào containerComment
                comments.forEach(function(comment) {
                    var commentHTML = `
                        <div id="comment_${comment.id}" class="comment">
                            <a href="/profile/${comment.authorId}">
                                <img class="avatar-comment" src="${comment.img}" alt="avatar"/>
                            </a>
                            <div class="comment-main-container">
                                <div class="comment-main">
                                    <p class="mb-1">
                                    <b>${comment.name}</b> <span class="small"> <i class="fa-solid fa-clock"></i> ${formatTime(comment.time)}</span>
                                    </p>
                                    <button onclick="deleleCmt(event, ${comment.id})"><i class="fa-solid fa-xmark"></i> </button>
                                </div>
                                <p class="comment-content">
                                ${comment.content}
                                </p>
                            </div>
                        </div>
                    `;
                    containerComment.innerHTML += commentHTML;
                });
            },
            error: function(error) {
                console.log(error);
            }
        });
    }

    function deleleCmt(event, commentId){ // xóa comment của mình thoi-----------
        // Gửi yêu cầu AJAX đến URL của Django view xử lý xóa dữ liệu
        var userChoice = window.confirm("Bạn có chắc muốn xóa bình luận không?");

        // Kiểm tra kết quả
        if (userChoice) {
        $.ajax({
            url: `/postspage/delete_comment/${commentId}/`,  // Điều chỉnh đúng đường dẫn của view xóa dữ liệu
            type: 'POST',
            data: { 'data_id': commentId },  // Truyền id của dữ liệu cần xóa
            success: function(response) {
                var containerComment = document.getElementById('comment_' + commentId);
                if(response.success === true){
                    containerComment.remove()
                    // Giảm _commentNum
                    const cmtNum = document.getElementById(response.postId + "_commentNum");
                    cmtNum.innerText = parseInt(cmtNum.innerText, 10) - 1
                    alert("Xóa bình luận của bạn thành công")
                }
                else{
                    alert("Không thể xóa bình luận của người khác!!!")
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
        }
    }

    function formatTime(timeString) {
        // Chuyển đổi chuỗi thời gian sang đối tượng Date

        const date = timeString.substring(0, timeString.indexOf('T'));
        const time = timeString.substring(timeString.indexOf('T') + 1, timeString.indexOf('T') + 6);
        // Định dạng lại thời gian theo ý muốn (ví dụ: dd/MM/yyyy HH:mm:ss)
        //const formattedTime = `${day}/${month}/${year} ${hours}:${minutes}:${seconds}`;
        const formattedTime = `${date} ${time}`;
        return formattedTime;
    }

    function showDetailPosts(event, postId ){
        $.ajax({
            url: `/postspage/search/detail/${postId}/`,
            type: 'POST',
            success: function(response) {
                var containerPost = document.getElementById("containerPost");
                containerPost.style.display = 'flex';
                var showADetailPost = document.getElementById("showADetailPost");

                detailPost = response.detailPost;
                var div1 = `
                    <div class="info">
                        <a href="">
                            <img src="${detailPost.authorAvatar}" alt="" class="avatar">
                        </a>
                        <h3><strong>${detailPost.authorName}</strong></h3>
                        <h6>Time: <strong> ${formatTime(detailPost.time)}</strong></h6>
                        <p>
                        Đang ở: <a href=""><strong>${detailPost.provider}</strong></a>
                        </p>
                    </div>
                    <h3><strong>${detailPost.title}</strong></h3>
                    <p>${detailPost.content}</p>
                    <div class="post-photo">
                `;
                // vòng for hiển thị các ảnh
                detailPost.img.forEach(function(img){
                    div1 += `
                    <img src="${img}" alt="Post 1" class="photo">
                    `;
                });

                div1 += `
                    </div>

                    <div class="post-actions">
                        <button value="false" onclick="likeAction(event, {{item.post.id}})">
                            <big id="${detailPost.like}_like">${detailPost.like}</big>
                            <i class="far fa-thumbs-up"></i>
                        </button>
                        <!-- Comment -->
                        <button onclick="showComment(event, {{ item.post.id }})">
                            <big id="${detailPost.cmt}_commentNum">${detailPost.cmt} </big>
                            <i class="far fa-comment"></i>
                        </button>
                        <!-- Heart -->
                        <i class="fa-regular fa-heart"></i>
                    </div>

                    <div class="post-comment">
                        <img src="" alt="" class="avatar">
                        <input type="text" placeholder="Viết bình luận ..." class="comment" id="${postId}_comment">
                        <button class="sendCmt" onclick="insertComment(event, ${postId})"> Gửi</button>
                    </div>
                `;
                showADetailPost.innerHTML = div1;
            },
            error: function(error) {
                console.log(error);
            }
        });
    }
    function cancelDetailPost(){
        var containerComment = document.getElementById('containerPost');
        containerComment.style.display = 'none'; // hoặc 'block' tùy thuộc vào yêu cầu của bạn
    }
  function cancelComment(){
    var containerComment = document.getElementById('containerComment');
    containerComment.style.display = 'none'; // hoặc 'block' tùy thuộc vào yêu cầu của bạn
  }