// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

contract ProductAuth {
    address public owner;
    uint256 private productCounter;

    // Product structure
    struct Product {
        uint productId;
        address payable seller;
        address buyer;
        bool isVerified;
        uint price;
        string imageHash;
    }

    // Mapping from product ID to product information
    mapping(uint => Product) public products;

    // Events
    event ProductVerified(uint productId, bool isReal);
    event ProductPurchased(
        uint productId,
        address buyer,
        address seller,
        uint price,
        string imageHash // Add imageHash to the event
    );

    // Constructor
    constructor() {
        owner = msg.sender;
        productCounter = 0;
    }

    // Modifiers
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }

    // Functions to handle incoming ETH
    receive() external payable {}
    fallback() external payable {}

    event ProductCreated(
        uint productId,
        address seller,
        uint price,
        string imageHash
    );

    function setProduct(
        uint _price,
        string memory _imageHash
    ) public returns (uint) {
        require(_price > 0, "Price must be greater than 0");

        productCounter++;
        uint newProductId = productCounter;

        products[newProductId] = Product({
            productId: newProductId,
            seller: payable(msg.sender),
            buyer: address(0),
            isVerified: false,
            price: _price,
            imageHash: _imageHash
        });

        emit ProductCreated(newProductId, msg.sender, _price, _imageHash);

        return newProductId;
    }

    function buyProduct(uint _productId) public payable {
        require(
            _productId <= productCounter && _productId > 0,
            "Invalid product ID"
        );
        Product storage product = products[_productId];
        require(product.seller != address(0), "Product does not exist");
        require(msg.value == product.price, "Incorrect Ether amount");
        require(product.buyer == address(0), "Product already sold");
        require(
            msg.sender != product.seller,
            "Seller cannot buy their own product"
        );

        product.buyer = msg.sender;

        // Emit event with imageHash included
        emit ProductPurchased(
            _productId,
            msg.sender,
            product.seller,
            product.price,
            product.imageHash
        );
    }

    function verifyProduct(
        uint _productId,
        string memory _imageHash
    ) public onlyOwner {
        require(
            _productId <= productCounter && _productId > 0,
            "Invalid product ID"
        );
        Product storage product = products[_productId];
        require(
            keccak256(bytes(product.imageHash)) == keccak256(bytes(_imageHash)),
            "Image hash mismatch"
        );

        // Your AI verification logic would go here
        product.isVerified = true;
        emit ProductVerified(_productId, true);
    }

    function realProduct(uint _productId) public {
        require(
            _productId <= productCounter && _productId > 0,
            "Invalid product ID"
        );
        Product storage product = products[_productId];
        require(product.seller != address(0), "Product does not exist");
        require(product.buyer != address(0), "No buyer for this product");
        require(!product.isVerified, "Product already verified");
        require(
            address(this).balance >= product.price,
            "Insufficient contract balance"
        );

        product.isVerified = true;

        (bool success, ) = product.seller.call{value: product.price}("");
        require(success, "Transfer failed");

        emit ProductVerified(_productId, true);
        emit ProductPurchased(
            _productId,
            product.buyer,
            product.seller,
            product.price,
            product.imageHash
        );
    }

    function fakeProduct(uint _productId) public {
        require(
            _productId <= productCounter && _productId > 0,
            "Invalid product ID"
        );
        Product storage product = products[_productId];
        require(product.seller != address(0), "Product does not exist");
        require(!product.isVerified, "Product already verified");

        if (product.buyer != address(0)) {
            (bool success, ) = payable(product.buyer).call{
                value: product.price
            }("");
            require(success, "Refund failed");
            product.buyer = address(0);
        }

        emit ProductVerified(_productId, false);
    }

    function getProduct(
        uint _productId
    ) public view returns (uint, address, address, bool, uint, string memory) {
        require(
            _productId <= productCounter && _productId > 0,
            "Invalid product ID"
        );
        Product memory product = products[_productId];
        return (
            product.productId,
            product.seller,
            product.buyer,
            product.isVerified,
            product.price,
            product.imageHash
        );
    }
}
