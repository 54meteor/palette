// SPDX-License-Identifier: GPL-3.0-or-later

pragma solidity ^0.6.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/SafeERC20.sol";
import "../interface/IAddrPower.sol";
import "../interface/IMiuToken.sol";

// JoyMaster is the source of joy. He can make Joy and he is a fair guy.

contract MiuMiuStakingMaster {
    using SafeMath for uint256;
    using SafeERC20 for IERC20;

    //
    // EVENTS
    //
    event Deposit(address indexed user, uint256 indexed pid, uint256 amount);
    event Withdraw(address indexed user, uint256 indexed pid, uint256 amount);
    event EmergencyWithdraw(address indexed user,uint256 indexed pid,uint256 amount);

    //
    // MODIFIERS
    //
    modifier notPause() {
        require(paused == false, "Master: Mining has been suspended");
        _;
    }

    //
    // enum and struct
    //

    // Info of each user.
    struct UserInfo {
        uint256 amount; // How many LP tokens the user has provided.
        uint256 rewardDebt; // Reward debt.
    }

    // Info of each pool.
    struct PoolInfo {
        IERC20 lpToken; // Address of LP token contract.
        uint256 allocPoint; // How many allocation points assigned to this pool.  to distribute per block.
        uint256 lastRewardBlock; // Last block number that  distribution occurs.
        uint256 accPerShare; // Accumulated MiuMius per share, times 1e12.
    }

    //**********************************************************//
    //    The below state variables can not change the order    //
    //**********************************************************//

    address public addrPower;
    // The Miu Token!
    IMiuToken public miu;
    // okens created per block.
    uint256 public miuPerBlock;
    // Info of each pool.
    PoolInfo[] public poolInfo;
    // Info of each user that stakes LP tokens.
    mapping(uint256 => mapping(address => UserInfo)) public userInfo;
    // pid corresponding address
    mapping(address => uint256) public LpOfPid;
    // Control mining
    bool public paused;
    // Total allocation points. Must be the sum of all allocation points in all pools.
    uint256 public totalAllocPoint;
    // The block number when miu mining starts.
    uint256 public startBlock;
    // How many blocks are halved
    uint256 public halvingPeriod;
    

    constructor (
        address _aPower,
        uint256 _miuPerBlock,
        uint256 _startBlock,
        uint256 _halvingPeriod
    ) public  {
        addrPower = _aPower;
        miuPerBlock = _miuPerBlock;
        startBlock = _startBlock;
        halvingPeriod = _halvingPeriod;
    }

    function poolLength() public view returns (uint256) {
        return poolInfo.length;
    }

    function setHalvingPeriod(uint256 _numberOfBlock) public onlyManager {
        halvingPeriod = _numberOfBlock;
    }

    function setMiuPerBlock(uint256 _newPerBlock) public onlyManager {
        massUpdatePools();
        miuPerBlock = _newPerBlock;
    }

    function setPause() public onlyManager {
        paused = !paused;
    }

    // Add a new lp to the pool. Can only be called by the owner.
    // XXX DO NOT add the same LP tokemigraten more than once. Rewards will be messed up if you do.
    function add(uint256 _allocPoint,IERC20 _lpToken,bool _withUpdate) public onlyManager {
        require(
            address(_lpToken) != address(0),"Master: _lpToken is the zero address");
        if (_withUpdate) {
            massUpdatePools();
        }
        uint256 lastRewardBlock = block.number > startBlock ? block.number : startBlock;
        totalAllocPoint = totalAllocPoint.add(_allocPoint);
        
        poolInfo.push(
            PoolInfo({
                lpToken: _lpToken,
                allocPoint: _allocPoint,
                lastRewardBlock: lastRewardBlock,
                accPerShare: 0
            })
        );
        LpOfPid[address(_lpToken)] = poolLength() - 1;
    }

    // Update the given pool's Miu allocation point. Can only be called by the owner.
    function set(uint256 _pid,uint256 _allocPoint,bool _withUpdate) public onlyManager {
        if (_withUpdate) {
            massUpdatePools();
        }
        totalAllocPoint = totalAllocPoint.sub(poolInfo[_pid].allocPoint).add(
            _allocPoint
        );
        poolInfo[_pid].allocPoint = _allocPoint;
    }

    function phase(uint256 blockNumber) public view returns (uint256) {
        if (halvingPeriod == 0) {
            return 0;
        }
        if (blockNumber > startBlock) {
            return (blockNumber.sub(startBlock).sub(1)).div(halvingPeriod);
        }
        return 0;
    }

    function reward(uint256 blockNumber) public view returns (uint256) {
        uint256 _phase = phase(blockNumber);
        return miuPerBlock.div(2**_phase);
    }

    function getMiuBlockReward(uint256 _lastRewardBlock)
        public
        view
        returns (uint256)
    {
        uint256 blockReward = 0;
        uint256 n = phase(_lastRewardBlock);
        uint256 m = phase(block.number);
        while (n < m) {
            n++;
            uint256 r = n.mul(halvingPeriod).add(startBlock);
            blockReward = blockReward.add(
                (r.sub(_lastRewardBlock)).mul(reward(r))
            );
            _lastRewardBlock = r;
        }
        blockReward = blockReward.add(
            (block.number.sub(_lastRewardBlock)).mul(reward(block.number))
        );
        return blockReward;
    }

    // Update reward variables for all pools. Be careful of gas spending!
    function massUpdatePools() public {
        uint256 length = poolInfo.length;
        for (uint256 pid = 0; pid < length; ++pid) {
            updatePool(pid);
        }
    }

    // Update reward variables of the given pool to be up-to-date.
    function updatePool(uint256 _pid) public {
        PoolInfo storage pool = poolInfo[_pid];
        if (block.number <= pool.lastRewardBlock) {
            return;
        }
        uint256 lpSupply = pool.lpToken.balanceOf(address(this));
        if (lpSupply == 0) {
            pool.lastRewardBlock = block.number;
            return;
        }

        uint256 blockReward = getMiuBlockReward(pool.lastRewardBlock);
        if (blockReward <= 0) {
            return;
        }
        uint256 miuReward = blockReward.mul(pool.allocPoint).div(totalAllocPoint);
        bool minRet = IMiuToken(nameAddr("MIUTOKEN")).mint(address(this), miuReward);
        //bool minRet;
        if (minRet) {
            pool.accPerShare = pool.accPerShare.add(miuReward.mul(1e12).div(lpSupply));
        }
        pool.lastRewardBlock = block.number;
    }

    // View function to see pending  on frontend.
    function pendingMiu(uint256 _pid, address _user)
        external
        view
        returns (uint256)
    {
        PoolInfo storage pool = poolInfo[_pid];
        UserInfo storage user = userInfo[_pid][_user];
        uint256 accPerShare = pool.accPerShare;
        uint256 lpSupply = pool.lpToken.balanceOf(address(this));
        if (user.amount > 0) {
            if (block.number > pool.lastRewardBlock) {
                uint256 blockReward = getMiuBlockReward(pool.lastRewardBlock);
                uint256 miuReward = blockReward.mul(pool.allocPoint).div(totalAllocPoint);
                accPerShare = accPerShare.add(miuReward.mul(1e12).div(lpSupply));
                
                return user.amount.mul(accPerShare).div(1e12).sub(user.rewardDebt);
            }
            if (block.number == pool.lastRewardBlock) {
                return user.amount.mul(accPerShare).div(1e12).sub(user.rewardDebt);
            }
        }
        return 0;
    }

    // Deposit LP tokens to Master for miu allocation.
    function deposit(uint256 _pid, uint256 _amount) public notPause {
        PoolInfo storage pool = poolInfo[_pid];
        UserInfo storage user = userInfo[_pid][msg.sender];
        updatePool(_pid);
        if (user.amount > 0) {
            uint256 pendingAmount =
                user.amount.mul(pool.accPerShare).div(1e12).sub(user.rewardDebt);
            if (pendingAmount > 0) {
                safeMiuTransfer(msg.sender, pendingAmount);
            }
        }
        if (_amount > 0) {
            pool.lpToken.safeTransferFrom(msg.sender, address(this), _amount);
            user.amount = user.amount.add(_amount);
        }
        user.rewardDebt = user.amount.mul(pool.accPerShare).div(1e12);
        emit Deposit(msg.sender, _pid, _amount);
    }

    // Withdraw LP tokens from Master.
    function withdraw(uint256 _pid, uint256 _amount) public notPause {
        PoolInfo storage pool = poolInfo[_pid];
        UserInfo storage user = userInfo[_pid][msg.sender];
        require(user.amount >= _amount, "Master: withdraw not good");
        updatePool(_pid);
        uint256 pendingAmount =
            user.amount.mul(pool.accPerShare).div(1e12).sub(user.rewardDebt);
        if (pendingAmount > 0) {
            safeMiuTransfer(msg.sender, pendingAmount);
        }
        if (_amount > 0) {
            user.amount = user.amount.sub(_amount);
            pool.lpToken.safeTransfer(msg.sender, _amount);
        }
        user.rewardDebt = user.amount.mul(pool.accPerShare).div(1e12);
        emit Withdraw(msg.sender, _pid, _amount);
    }

    // Withdraw without caring about rewards. EMERGENCY ONLY.
    function emergencyWithdraw(uint256 _pid) public notPause {
        PoolInfo storage pool = poolInfo[_pid];
        UserInfo storage user = userInfo[_pid][msg.sender];
        uint256 amount = user.amount;
        user.amount = 0;
        user.rewardDebt = 0;
        pool.lpToken.safeTransfer(address(msg.sender), amount);
        emit EmergencyWithdraw(msg.sender, _pid, amount);
    }

    // Safe  transfer function, just in case if rounding error causes pool to not have enough JOYs.
    function safeMiuTransfer(address _to, uint256 _amount) internal {
        uint256 joyBal = IMiuToken(nameAddr("MIUTOKEN")).balanceOf(address(this));
        if (_amount > joyBal) {
            IMiuToken(nameAddr("MIUTOKEN")).transfer(_to, joyBal);
        } else {
            IMiuToken(nameAddr("MIUTOKEN")).transfer(_to, _amount);
        }
    }
    
    function nameAddr(string memory _name) internal view returns(address){
        return IAddrPower(addrPower).getAddr(_name);
    }
    
    modifier onlyManager(){
        require(IAddrPower(addrPower).isManager(msg.sender),"onlyManager");
        _;
    }
}
