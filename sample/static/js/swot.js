console.log("swot.jsが読み込まれました");

function addInputField(elementId) {
    // 新しい入力欄を生成
    var newInput = document.createElement('input');
    newInput.type = 'text';
    newInput.name = elementId;
    newInput.placeholder = 'Enter something';

    // 改行を追加
    var lineBreak = document.createElement('br');

    // ボタンの前に新しい入力欄と改行を挿入
    var addButton = document.getElementById(elementId + '_add');
    addButton.parentNode.insertBefore(newInput, addButton);
    addButton.parentNode.insertBefore(lineBreak, addButton);
}