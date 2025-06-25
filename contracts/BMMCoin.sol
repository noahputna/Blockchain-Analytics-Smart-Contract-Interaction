// Import standard ERC-20 interface.
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

// A simple ERC-20 token called BMMCoin.
contract BMMCoin is ERC20 {
    constructor(uint256 initialSupply) ERC20("BMMCoin", "BMM") {
        _mint(msg.sender, initialSupply);
    }

    // Allow students to request free tokens (faucet-style).
    function request(uint256 amount) public {
        _mint(msg.sender, amount);
    }
}