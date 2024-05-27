console.log("swot.jsが読み込まれました");

function addInputField(elementId) {
    console.log('こっちは');
    // 新しい入力欄を生成
    var newInput = document.createElement('input');
    newInput.type = 'text';
    // newInput.name = elementId;
    newInput.name = elementId + '_' + document.querySelectorAll('input[type="text"][name^="' + elementId + '"]').length; // 例: strengths_1, strengths_2, ...
    newInput.placeholder = 'Enter something';

    // 改行を追加
    var lineBreak = document.createElement('br');

    // ボタンの前に新しい入力欄と改行を挿入
    var addButton = document.getElementById(elementId + '_add');
    addButton.parentNode.insertBefore(newInput, addButton);
    addButton.parentNode.insertBefore(lineBreak, addButton);
}

// 送信ボタンをクリックする
// 送信ボタンをクリックする
function submitForm() {
    console.log('入った');
    // 追加された要素をフォームに追加
    addDynamicInputsToForm();
    // フォームを送信
    document.getElementById('add_swot').submit();
}

// フォームに追加された動的要素をフォームに追加する
function addDynamicInputsToForm() {
    var form = document.getElementById('add_swot');
    var dynamicInputs = document.querySelectorAll('input[type="text"]:not([name="title"])');
    console.log(dynamicInputs);
    dynamicInputs.forEach(function(input) {
        // フォームに動的要素を追加
        form.appendChild(input);
    });
    console.log(form);
}