// カイジ風「ざわ。。。」を出現させるjs
function displayZawa(top, left, scale) {
    const imageElement = document.createElement("img");
    imageElement.src = "../image/zawa.png";

    imageElement.style.position = "fixed";
    imageElement.style.top = top;
    imageElement.style.left = left;
    imageElement.style.opacity = "0";
    imageElement.style.width = scale; 
    imageElement.style.height = "auto"; 

    document.body.appendChild(imageElement);
    // フェードアニメーションの設定
    fadeInOutAnimation(imageElement);
}

function fadeInOutAnimation(ie){
    // フェードインアニメーション
    const fadein = ie.animate(
        [{ opacity: "0" }, { opacity: "1" }],
        {
            duration: 1000, // アニメーションの時間（ミリ秒）
            fill: "forwards" // アニメーションの最後のフレームを保持
        }
    )

    // 遅れてフェードアウトアニメーション
    fadein.onfinish = setTimeout(() => {
        ie.animate(
            [{ opacity: "1" }, { opacity: "0" }],
            {
                duration: 1000, // アニメーションの時間（ミリ秒）
                fill: "forwards" // アニメーションの最後のフレームを保持
            }
        ).onfinish = () => {
            document.body.removeChild(ie);
        };
    }, 1500)
}

function generateRandomList(n) {
    const numbers = Array.from({ length: n }, (_, index) => index + 1); // 1からnまでの整数を含む配列を生成
    const shuffledNumbers = [];
    while (numbers.length > 0) {
    const randomIndex = Math.floor(Math.random() * numbers.length);
    const removedElement = numbers.splice(randomIndex, 1)[0];
    shuffledNumbers.push(removedElement);
    }
    return shuffledNumbers;
}

const n = 5;
const randomList1 = generateRandomList(n);
const randomList2 = generateRandomList(n);
console.log(randomList1);
console.log(randomList2);

let i = 0;
// 0.2秒ごとに関数を呼び出す
const interval = setInterval(() => {
    // const max_width = 900; const max_height = 600;
    const left = (randomList1[i]-1)*20 + "%";
    const top = (randomList2[i]-1)*20 + "%";
    const scale = (20 + Number(Math.round(Math.random()*20))) + "%";
    displayZawa(top, left, scale);
    console.log(top);
    console.log(scale);
    console.log(i);
    i++;
}, 200); 

// 1秒後に繰り返し処理を停止する
setTimeout(() => {
    clearInterval(interval); 
}, 1000);
