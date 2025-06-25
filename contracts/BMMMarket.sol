// Import standard ERC-20 interface.
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

// BMMMarket allows users to purchase products A, B, or C using BMMCoin.
contract BMMMarket {
    IERC20 public bmmCoin;

    // Product prices stored per ID.
    mapping(string => uint256) public productFees;
    mapping(string => uint256) public productSales;

    constructor(address _tokenAddress) {
        bmmCoin = IERC20(_tokenAddress);

        // Set initial product prices (in BMM).
        productFees["A"] = 10 * 1e18;
        productFees["B"] = 20 * 1e18;
        productFees["C"] = 30 * 1e18;
    }

    // Allows a user to buy a product by transferring BMM tokens to the contract.
    function buyProduct(string memory productId) public {
        uint256 fee = productFees[productId];
        require(fee > 0, "Invalid product");

        // Transfer BMM tokens from user to contract (user must approve first).
        bool success = bmmCoin.transferFrom(msg.sender, address(this), fee);
        require(success, "Transfer failed");

        // Track number of purchases.
        productSales[productId]++;
    }

    // Get fee for frontend or off-chain access.
    function getFee(string memory productId) public view returns (uint256) {
        return productFees[productId];
    }
}