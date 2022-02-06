// SPDX-License-Identifier: MIT
pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract SimpleCollectible is ERC721 {
    uint256 public tokenCounter;
    constructor () public ERC721 ("NFT Bridge", "NFT"){
        tokenCounter = 0;
    }

    function createCollectible(address newAddress, string memory tokenURI) public returns (uint256) {
        uint256 newItemId = tokenCounter;
        _safeMint(newAddress, newItemId);
        _setTokenURI(newItemId, tokenURI);
        tokenCounter = tokenCounter + 1;
        return newItemId;
    }

}
