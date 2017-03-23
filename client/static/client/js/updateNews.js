$(function(){
    $("input[name='publish']").click(function(){
        newsId = ""
        $newsContent=$("textarea[name='newsContent']")
        $newsContent.html(CKEDITOR.instances.editor.getData())
        $(".news-box").attr("action","/update")
        $.ajaxSetup({});
        $(".news-box").ajaxSubmit
        ({
            resetForm:false,
            dataType:'json',
            success:function(data){
              if (data==1){
                  alert("发布成功！");
              }else if (data==2){
                  alert("修改成功！");
              }else{
                  alert("操作失败");
                  return ;
              }
              location.href="/admin";
            }
        });
    });
})
