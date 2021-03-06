pragma solidity >= 0.5.10;

interface IERC20 {
    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function transfer(address recipient, uint256 amount) external returns (bool);
    function allowance(address owner, address spender) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}

library SafeMath {

    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        require(c >= a, "SafeMath: addition overflow");

        return c;
    }

    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        return sub(a, b, "SafeMath: subtraction overflow");
    }


    function sub(uint256 a, uint256 b, string memory errorMessage) internal pure returns (uint256) {
        require(b <= a, errorMessage);
        uint256 c = a - b;

        return c;
    }


    function mul(uint256 a, uint256 b) internal pure returns (uint256) {
       if (a == 0) {
            return 0;
        }

        uint256 c = a * b;
        require(c / a == b, "SafeMath: multiplication overflow");

        return c;
    }


    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        return div(a, b, "SafeMath: division by zero");
    }


    function div(uint256 a, uint256 b, string memory errorMessage) internal pure returns (uint256) {
        require(b > 0, errorMessage);
        uint256 c = a / b;
        // assert(a == b * c + a % b); // There is no case in which this doesn't hold

        return c;
    }


    function mod(uint256 a, uint256 b) internal pure returns (uint256) {
        return mod(a, b, "SafeMath: modulo by zero");
    }


    function mod(uint256 a, uint256 b, string memory errorMessage) internal pure returns (uint256) {
        require(b != 0, errorMessage);
        return a % b;
    }
}

library Address {
    /**
     * @dev Returns true if `account` is a contract.
     *
     * [IMPORTANT]
     * ====
     * It is unsafe to assume that an address for which this function returns
     * false is an externally-owned account (EOA) and not a contract.
     *
     * Among others, `isContract` will return false for the following 
     * types of addresses:
     *
     *  - an externally-owned account
     *  - a contract in construction
     *  - an address where a contract will be created
     *  - an address where a contract lived, but was destroyed
     * ====
     */
    function isContract(address account) internal view returns (bool) {
        // According to EIP-1052, 0x0 is the value returned for not-yet created accounts
        // and 0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470 is returned
        // for accounts without code, i.e. `keccak256('')`
        bytes32 codehash;
        bytes32 accountHash = 0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470;
        // solhint-disable-next-line no-inline-assembly
        assembly { codehash := extcodehash(account) }
        return (codehash != accountHash && codehash != 0x0);
    }

    /**
     * @dev Converts an `address` into `address payable`. Note that this is
     * simply a type cast: the actual underlying value is not changed.
     *
     * _Available since v2.4.0._
     */
    function toPayable(address account) internal pure returns (address payable) {
        return address(uint160(account));
    }

    /**
     * @dev Replacement for Solidity's `transfer`: sends `amount` wei to
     * `recipient`, forwarding all available gas and reverting on errors.
     *
     * https://eips.ethereum.org/EIPS/eip-1884[EIP1884] increases the gas cost
     * of certain opcodes, possibly making contracts go over the 2300 gas limit
     * imposed by `transfer`, making them unable to receive funds via
     * `transfer`. {sendValue} removes this limitation.
     *
     * https://diligence.consensys.net/posts/2019/09/stop-using-soliditys-transfer-now/[Learn more].
     *
     * IMPORTANT: because control is transferred to `recipient`, care must be
     * taken to not create reentrancy vulnerabilities. Consider using
     * {ReentrancyGuard} or the
     * https://solidity.readthedocs.io/en/v0.5.11/security-considerations.html#use-the-checks-effects-interactions-pattern[checks-effects-interactions pattern].
     *
     * _Available since v2.4.0._
     */
    function sendValue(address payable recipient, uint256 amount) internal {
        require(address(this).balance >= amount, "Address: insufficient balance");

        // solhint-disable-next-line avoid-call-value
        (bool success, ) = recipient.call.value(amount)("");
        require(success, "Address: unable to send value, recipient may have reverted");
    }
}

library SafeERC20 {
    using SafeMath for uint256;
    using Address for address;

    function safeTransfer(IERC20 token, address to, uint256 value) internal {
        callOptionalReturn(token, abi.encodeWithSelector(token.transfer.selector, to, value));
    }

    function safeTransferFrom(IERC20 token, address from, address to, uint256 value) internal {
        callOptionalReturn(token, abi.encodeWithSelector(token.transferFrom.selector, from, to, value));
    }

    function safeApprove(IERC20 token, address spender, uint256 value) internal {
        // safeApprove should only be called when setting an initial allowance,
        // or when resetting it to zero. To increase and decrease it, use
        // 'safeIncreaseAllowance' and 'safeDecreaseAllowance'
        // solhint-disable-next-line max-line-length
        require((value == 0) || (token.allowance(address(this), spender) == 0),
            "SafeERC20: approve from non-zero to non-zero allowance"
        );
        callOptionalReturn(token, abi.encodeWithSelector(token.approve.selector, spender, value));
    }

    function safeIncreaseAllowance(IERC20 token, address spender, uint256 value) internal {
        uint256 newAllowance = token.allowance(address(this), spender).add(value);
        callOptionalReturn(token, abi.encodeWithSelector(token.approve.selector, spender, newAllowance));
    }

    function safeDecreaseAllowance(IERC20 token, address spender, uint256 value) internal {
        uint256 newAllowance = token.allowance(address(this), spender).sub(value, "SafeERC20: decreased allowance below zero");
        callOptionalReturn(token, abi.encodeWithSelector(token.approve.selector, spender, newAllowance));
    }

    /**
     * @dev Imitates a Solidity high-level call (i.e. a regular function call to a contract), relaxing the requirement
     * on the return value: the return value is optional (but if data is returned, it must not be false).
     * @param token The token targeted by the call.
     * @param data The call data (encoded using abi.encode or one of its variants).
     */
    function callOptionalReturn(IERC20 token, bytes memory data) private {
        // We need to perform a low level call here, to bypass Solidity's return data size checking mechanism, since
        // we're implementing it ourselves.

        // A Solidity high level call has three parts:
        //  1. The target address is checked to verify it contains contract code
        //  2. The call itself is made, and success asserted
        //  3. The return value is decoded, which in turn checks the size of the returned data.
        // solhint-disable-next-line max-line-length
        // require(address(token).isContract(), "SafeERC20: call to non-contract");

        // solhint-disable-next-line avoid-low-level-calls
        (bool success, bytes memory returndata) = address(token).call(data);
        require(success, "SafeERC20: low-level call failed");

        if (returndata.length > 0) { // Return data is optional
            // solhint-disable-next-line max-line-length
            require(abi.decode(returndata, (bool)), "SafeERC20: ERC20 operation did not succeed");
        }
    }
}

contract Context {
    // Empty internal constructor, to prevent people from mistakenly deploying
    // an instance of this contract, which should be used via inheritance.
    constructor () internal { }
    // solhint-disable-previous-line no-empty-blocks

    function _msgSender() internal view returns (address payable) {
        return msg.sender;
    }

    function _msgData() internal view returns (bytes memory) {
        this; // silence state mutability warning without generating bytecode - see https://github.com/ethereum/solidity/issues/2691
        return msg.data;
    }
}

contract Ownable is Context {
    address private _owner;

    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    /**
     * @dev Initializes the contract setting the deployer as the initial owner.
     */
    constructor () internal {
        address msgSender = _msgSender();
        _owner = msgSender;
        emit OwnershipTransferred(address(0), msgSender);
    }

    /**
     * @dev Returns the address of the current owner.
     */
    function owner() public view returns (address) {
        return _owner;
    }

    /**
     * @dev Throws if called by any account other than the owner.
     */
    modifier onlyOwner() {
        require(isOwner(), "Ownable: caller is not the owner");
        _;
    }

    /**
     * @dev Returns true if the caller is the current owner.
     */
    function isOwner() public view returns (bool) {
        return _msgSender() == _owner;
    }

    /**
     * @dev Leaves the contract without owner. It will not be possible to call
     * `onlyOwner` functions anymore. Can only be called by the current owner.
     *
     * NOTE: Renouncing ownership will leave the contract without an owner,
     * thereby removing any functionality that is only available to the owner.
     */
    function renounceOwnership() public onlyOwner {
        emit OwnershipTransferred(_owner, address(0));
        _owner = address(0);
    }

    /**
     * @dev Transfers ownership of the contract to a new account (`newOwner`).
     * Can only be called by the current owner.
     */
    function transferOwnership(address newOwner) public onlyOwner {
        _transferOwnership(newOwner);
    }

    /**
     * @dev Transfers ownership of the contract to a new account (`newOwner`).
     */
    function _transferOwnership(address newOwner) internal {
        require(newOwner != address(0), "Ownable: new owner is the zero address");
        emit OwnershipTransferred(_owner, newOwner);
        _owner = newOwner;
    }
}

contract BBCBill is Ownable {
    
    using SafeMath for uint256;
    using SafeERC20 for IERC20;
    // event
    event debug(uint256 msg);
    event inflowEvent(address owner, uint256 amount, uint256 rate, address indexed contractAddress,
                string bbcBranch, string bbcAddress, bytes32 primaryKey);
    event retraceEvent(address indexed _to, uint256 _amount);
    event withdrawEvent(address indexed _to, uint256 _amount);
    //struct
    struct InFlow{
        uint256 amount;//金额
        uint256 rate;//汇率
        address contractAddress ;//代币合约地址
        string bbcBranch;//bbc分支标识
        string bbcAddress;//bbc接收地址
    }

    struct Retrace{
        uint256 txid;//流入交易txid
        uint256 amount;//金额
        address payable walletAddress;//接收钱包地址
        address contractAddress;//代币合约地址
        uint256 fee;//手续费
    }

    struct OutFlow{
        string bbcTxid;//bbc流入txid
        string bbcBranch;//bbc分支标识
        address payable walletAddress;//接收者钱包地址
        address contractAddress;//代币合约地址
        uint256 amount;//金额
    }

    mapping(address => mapping(bytes32 => InFlow)) public inFlowList;
    mapping(address => mapping(bytes32 => Retrace)) public retraceList;
    mapping(address => mapping(bytes32 => OutFlow)) public outFlowList;

    function getInFlow(address owner, bytes32 primarykey) public view returns(
        uint256 amount, uint256 rate, address contracAddress,
        string memory bbcBranch, string memory bbcAddress){
        return (
            inFlowList[owner][primarykey].amount, inFlowList[owner][primarykey].rate,
            inFlowList[owner][primarykey].contractAddress,
            inFlowList[owner][primarykey].bbcBranch,
            inFlowList[owner][primarykey].bbcAddress
        );
    }

    function getRetrace(address owner, bytes32 primarykey) public view returns(
        uint256 txid, uint256 amount, address walletAddress, address contracAddress,
        uint256 fee
    ){
        return (
            retraceList[owner][primarykey].txid, retraceList[owner][primarykey].amount,
            retraceList[owner][primarykey].walletAddress,
            retraceList[owner][primarykey].contractAddress, retraceList[owner][primarykey].fee
        );
    }

    function getOutFlow(address owner, bytes32 primarykey) public view returns(
        string memory bbcTxid, string memory bbcBranch,address walletAddress,
        address contractAddress, uint256 amount
    ){
        return (
            outFlowList[owner][primarykey].bbcTxid, outFlowList[owner][primarykey].bbcBranch,
            outFlowList[owner][primarykey].walletAddress,
            outFlowList[owner][primarykey].contractAddress, outFlowList[owner][primarykey].amount
        );
    }

    function inFlow(uint256 _amount, uint256 _rate, address _contractAddress,
                string memory _bbcBranch, string memory _bbcAddress, bytes32 _primaryKey) public payable returns(bool){
        require(_amount > 0,"inFlow:_amount invalid");
        require(inFlowList[msg.sender][_primaryKey].amount == 0,"InFlow: primaryKey is exist()");
        if ( msg.value > 0 ) {
            _contractAddress = address(0);
            _amount = msg.value;
        }else{
            IERC20(_contractAddress).safeTransferFrom(msg.sender, address(this), _amount);
        }
        inFlowList[msg.sender][_primaryKey] = InFlow({
                amount:_amount, rate:_rate,
                contractAddress:_contractAddress,
                bbcBranch:_bbcBranch,
                bbcAddress:_bbcAddress});
        emit inflowEvent(msg.sender, _amount,_rate,_contractAddress,_bbcBranch,_bbcAddress,_primaryKey);
        return true;
    }

    function retrace(uint256 _txid, uint256 _amount, address payable _walletAddress, address _contractAddress,
        uint256 _fee, bytes32 _primaryKey) public onlyOwner returns(bool){
        require(_amount > 0,"retrace:_amount invalid");
        require(inFlowList[msg.sender][_primaryKey].amount == 0,"retrace: primaryKey is exist()");
        retraceList[_walletAddress][_primaryKey] = Retrace({
                txid: _txid,
                amount: _amount,
                walletAddress: _walletAddress,
                contractAddress: _contractAddress,
                fee: _fee
        });
//        if(orderList[msg.sender][ordrePrimaryKey].tradePair['trade'].sellToken == address(0)){
//                    msg.sender.transfer(_amount);
//                }else{
//                    IERC20(orderList[msg.sender][ordrePrimaryKey].tradePair['trade'].sellToken).safeTransfer(msg.sender, _amount);
//                }
        return true;
    }

    function withDraw(string memory _txid, string memory _bbcBranch, address payable _walletAddress,
        address _contractAddress, uint256 _amount, bytes32 _primaryKey) public onlyOwner returns(bool){
        require(_amount > 0,"withDraw:_amount invalid");
        require(inFlowList[msg.sender][_primaryKey].amount == 0,"withDraw: primaryKey is exist()");
        outFlowList[_walletAddress][_primaryKey] = OutFlow({
                bbcTxid: _txid,
                bbcBranch: _bbcBranch,
                walletAddress: _walletAddress,
                contractAddress: _contractAddress,
                amount: _amount
        });
//        if(orderList[orderAddress][ordrePrimaryKey].tradePair['trade'].sellToken == address(0)){
//                    between.buyAddress.transfer(buyAmount);
//                    msg.sender.transfer(exchange);
//                    betweensAddress.transfer(exchange);
//                }else{
//                    IERC20(orderList[orderAddress][ordrePrimaryKey].tradePair['trade'].sellToken).safeTransfer(between.buyAddress, buyAmount);
//                    //给撮合者转账
//                    IERC20(orderList[orderAddress][ordrePrimaryKey].tradePair['trade'].sellToken).safeTransfer(betweensAddress, exchange);
//                    //给执行者转账
//                    IERC20(orderList[orderAddress][ordrePrimaryKey].tradePair['trade'].sellToken).safeTransfer(msg.sender, exchange);
//                }
        return true;
    }
    

//     function carryOut( bytes32 randI,  bytes32 randJ, address orderAddress,address payable betweensAddress,
//                bytes32 ordrePrimaryKey,bytes32 betweenPrimaryKey) public {
//            uint256 blockNo = orderList[orderAddress][ordrePrimaryKey].blockHeight
//                .add(orderList[orderAddress][ordrePrimaryKey].betweens[betweenPrimaryKey].blockNo);
//            require( block.number < blockNo,"carryOut:blockHeight invalid");
//
//            GoBetween memory between = orderList[orderAddress][ordrePrimaryKey].betweens[betweenPrimaryKey];
//
//            require(between.carryOut == msg.sender,"carryOut:caller is not the carryOut");
//            require(checkHash(randI,between.randIHash),"carryOut:randI invalid");
//            require(checkHash(randJ,between.randJHash),"carryOut:randJ invalid");
//            require(between.sellAmount > 0,"carryOut:sellAmount not enough");
//                //可交易总额度
//                uint256 totalAmount = between.sellAmount;
//                //计算手续费（手续费= fee / 10000)
//                uint256 fee = totalAmount.mul(orderList[orderAddress][ordrePrimaryKey].fee).div(10000);
//                //计算转给乙方的数量
//                uint256 buyAmount = totalAmount.sub(fee);
//                //计算撮合者及执行者的收益
//                uint256 exchange = fee.div(2);
//                //可用额度置0
//                orderList[orderAddress][ordrePrimaryKey].betweens[betweenPrimaryKey].sellAmount = 0;
//                //给乙方转账
//
//                if(orderList[orderAddress][ordrePrimaryKey].tradePair['trade'].sellToken == address(0)){
//                    between.buyAddress.transfer(buyAmount);
//                    msg.sender.transfer(exchange);
//                    betweensAddress.transfer(exchange);
//                }else{
//                    IERC20(orderList[orderAddress][ordrePrimaryKey].tradePair['trade'].sellToken).safeTransfer(between.buyAddress, buyAmount);
//                    //给撮合者转账
//                    IERC20(orderList[orderAddress][ordrePrimaryKey].tradePair['trade'].sellToken).safeTransfer(betweensAddress, exchange);
//                    //给执行者转账
//                    IERC20(orderList[orderAddress][ordrePrimaryKey].tradePair['trade'].sellToken).safeTransfer(msg.sender, exchange);
//                }
//                emit withdrawEvent(between.buyAddress,buyAmount);
//                emit withdrawEvent(betweensAddress,exchange);
//                emit withdrawEvent(msg.sender,exchange);
//     }
//    // // withdraw
//    // /**
//    //  * 返回用户代币
//    //  */
//    function retrace(bytes32 ordrePrimaryKey) public returns(bool) {
//            uint256 _amount = orderList[msg.sender][ordrePrimaryKey].tradePair['trade'].sellAmount;
//            orderList[msg.sender][ordrePrimaryKey].tradePair['trade'].sellAmount
//                = orderList[msg.sender][ordrePrimaryKey].tradePair['trade'].sellAmount.sub(_amount);
//                bytes32[] memory keys = orderList[msg.sender][ordrePrimaryKey].betweensKeys[ordrePrimaryKey];
//                for(uint j = 0; j < keys.length; j++){
//                    uint256 blockNo = orderList[msg.sender][ordrePrimaryKey].blockHeight
//                            .add(orderList[msg.sender][ordrePrimaryKey].betweens[keys[j]].blockNo);
//                    if (block.number > blockNo){
//                        _amount = _amount.add(orderList[msg.sender][ordrePrimaryKey].betweens[keys[j]].sellAmount);
//                    }
//
//                }
//                if(orderList[msg.sender][ordrePrimaryKey].tradePair['trade'].sellToken == address(0)){
//                    msg.sender.transfer(_amount);
//                }else{
//                    IERC20(orderList[msg.sender][ordrePrimaryKey].tradePair['trade'].sellToken).safeTransfer(msg.sender, _amount);
//                }
//                emit retraceEvent(msg.sender, _amount);
//
//        return true;
//    }
}