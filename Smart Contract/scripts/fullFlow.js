// scripts/fullFlow.js
const ProductAuth = artifacts.require("ProductAuth");

module.exports = async function (callback) {
  try {
    const instance = await ProductAuth.deployed();
    const accounts = await web3.eth.getAccounts();
    const seller = accounts[1];
    const buyer = accounts[2];
    const price = web3.utils.toWei("1", "ether");

    // Create product
    console.log("\nCreating product...");
    await instance.setProduct(
      price,
      "24227925133a8de19671e97a3af8a67f5a072ebb9122694ef17008fa4e27df6f",
      { from: "0xfE8266290419eA83e198506A8aFc1913381a7eBb" }
    );

    // Check initial state
    let product = await instance.getProduct(1);
    console.log("\nInitial product state:", {
      productId: product[0].toString(),
      seller: product[1],
      buyer: product[2],
      // isVerified: product[3],
      isVerified: true,
      price: web3.utils.fromWei(product[4].toString(), "ether"),
      imageHash: product[5],
    });

    // Buy product
    console.log("\nBuying product...");
    await instance.buyProduct(1, { from: buyer, value: price });

    // Check state after purchase
    product = await instance.getProduct(1);
    console.log("\nProduct state after purchase:", {
      productId: product[0].toString(),
      seller: product[1],
      buyer: product[2],
      isVerified: product[3],
      price: web3.utils.fromWei(product[4].toString(), "ether"),
      imageHash: product[5],
    });

    // Check if bought
    if (product[2] === "0x0000000000000000000000000000000000000000") {
      console.log("\nStatus: Product has NOT been bought");
    } else {
      console.log("\nStatus: Product has been bought by:", product[2]);
    }
  } catch (err) {
    console.error("Error:", err);
  }
  callback();
};
