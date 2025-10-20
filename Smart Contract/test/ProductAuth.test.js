const ProductAuth = artifacts.require("ProductAuth");
const chai = require("chai");
const assert = chai.assert;
const truffleAssert = require("truffle-assertions");

contract("ProductAuth", (accounts) => {
  let productAuth;
  const owner = accounts[0];
  const seller = accounts[1];
  const buyer = accounts[2];
  const price = web3.utils.toWei("1", "ether");
  const imageHash = "QmTest123";

  beforeEach(async () => {
    productAuth = await ProductAuth.new({ from: owner });
  });

  it("should set the correct owner", async () => {
    const contractOwner = await productAuth.owner();
    assert.equal(contractOwner, owner, "Owner not set correctly");
  });

  it("should create a new product with correct details", async () => {
    const tx = await productAuth.setProduct(price, imageHash, { from: seller });
    const productId = 1; // First product should have ID 1

    const product = await productAuth.getProduct(productId);
    assert.equal(product[1], seller, "Seller address incorrect");
    assert.equal(product[4].toString(), price, "Price incorrect");
    assert.equal(product[5], imageHash, "Image hash incorrect");
  });

  it("should not allow product creation with zero price", async () => {
    await truffleAssert.reverts(
      productAuth.setProduct(0, imageHash, { from: seller }),
      "Price must be greater than 0"
    );
  });

  it("should allow purchase with correct amount", async () => {
    // Create product first
    await productAuth.setProduct(price, imageHash, { from: seller });

    const tx = await productAuth.buyProduct(1, {
      from: buyer,
      value: price,
    });

    // Verify the purchase event was emitted
    truffleAssert.eventEmitted(tx, "ProductPurchased", (ev) => {
      return ev.buyer === buyer && ev.price.toString() === price.toString();
    });

    // Check product details after purchase
    const product = await productAuth.getProduct(1);
    assert.equal(product[2], buyer, "Buyer not set correctly");
  });

  it("should allow marking product as fake and refund buyer", async () => {
    // Create and buy product first
    await productAuth.setProduct(price, imageHash, { from: seller });
    await productAuth.buyProduct(1, { from: buyer, value: price });

    const tx = await productAuth.fakeProduct(1, { from: owner });

    // Verify ProductVerified event was emitted with isReal = false
    truffleAssert.eventEmitted(tx, "ProductVerified", (ev) => {
      return ev.productId.toString() === "1" && ev.isReal === false;
    });
  });
});
