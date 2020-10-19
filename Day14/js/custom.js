/**
* Created by wenchong on 16/11/15.
*/

function LineEditEnd(ths){
    if($("#edit-check").hasClass("editing")){
        // 使 input[name='vol'] 所在的行其他列退出编辑模式
        $(ths).parent().siblings().each(function () {
            var val = $(this).children().val();
            $(this).text(val);
            $(this).removeClass("editing")
        })
    }
}

function LineEditStart(ths){
    if($("#edit-check").hasClass("editing")){
        // 使 input[name='vol'] 所在的行其他列进入编辑模式
        $(ths).parent().siblings().each(function () {
            if(! $(this).hasClass("editing")) {
                // 获取原来的内容
                var val = $(this).text();
                // 创建新的 input 标签
                var tag = document.createElement("input");
                tag.type = "text";
                tag.value = val;
                // 将原来的内容修改为 input
                $(this).html(tag);
                $(this).addClass("editing")
            }
        })
    }
}

function EnterEditing(){
    // 修改按钮的 value 为退出编辑模式，并添加 editing 类
    $("#edit-check").val("退出编辑模式");
    $("#edit-check").addClass("editing");
}

function ExitEditing(){
    // 修改按钮的 value 为进入编辑模式，并删除 editing 类
    $("#edit-check").val("进入编辑模式");
    $("#edit-check").removeClass("editing");
}

function CheckAll(){
    $("#tb tbody input[name='vol']").each(function () {
        $(this).prop('checked',true);
        LineEditStart(this)
    });
}

function CancelAll(){
    $("#tb tbody input[name='vol']").each(function () {
        $(this).prop('checked',false);
        LineEditEnd(this)
    });
}

function ReverseAll(){
    $("#tb tbody input[name='vol']").each(function(){
        if($(this).prop('checked')){
            $(this).prop('checked',false);
            LineEditEnd(this)
        }else{
            $(this).prop('checked', true);
            LineEditStart(this)
        }
    });
}

function AloneCheck(){
    if($("#edit-check").hasClass('editing')){
        if($(this).prop('checked') == false){
            LineEditEnd(this);
        }else{
            LineEditStart(this);
        }
    }
}

function EditCheck(){
    if($("#edit-check").hasClass('editing')){
        $("#tb input[name='vol']").each(function () {
                if($(this).prop('checked')){
                    LineEditEnd(this);
                }
            }
        );
        ExitEditing();

    }else{
        EnterEditing();
        $("#tb input[name='vol']").each(function () {
            if($(this).prop('checked')){
                LineEditStart(this)
            }
        });
    }
}
