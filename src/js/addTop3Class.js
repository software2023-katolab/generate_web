function addClassToTop3() {
    const table = document.getElementById("data-table");
    const rows = table.getElementsByTagName("tr");
    const numColumns = rows[0].getElementsByTagName("td").length;

    // 各列の値を格納する2次元配列を初期化
    const columnValues = new Array(numColumns).fill().map(() => []);

    // 各列の値を2次元配列に格納する
    for (let i = 0; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName("td");
        for (let j = 0; j < numColumns; j++) {
            const cellValue = parseFloat(cells[j].textContent);
            columnValues[j].push(cellValue);
        }
    }

    // 各列の値を降順にソートする
    for (let j = 0; j < numColumns; j++) {
        columnValues[j].sort((a, b) => b - a);
    }

    // 最大値に"top1"クラスを追加
    for (let i = 0; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName("td");
        for (let j = 0; j < numColumns; j++) {
            const cellValue = parseFloat(cells[j].textContent);
            if (cellValue === columnValues[j][0]) {
                cells[j].classList.add("top1");
            } else if (cellValue === columnValues[j][1]) {
                cells[j].classList.add("top2");
            } else if (cellValue === columnValues[j][2]) {
                cells[j].classList.add("top3");
            }
        }
    }
}

// プログラムを実行
addClassToTop3();
