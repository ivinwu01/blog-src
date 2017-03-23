$(function(){
    $("input[name='publish']").click(function(){
        $newsContent=$("textarea[name='blogContent']")
        $newsContent.html(CKEDITOR.instances.editor.getData())
        $(".blog-box").attr("action","/cms/update")
        $.ajaxSetup({});
        $(".blog-box").ajaxSubmit
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
              location.href="/cms/blogsList";
            }
        });
    });
})