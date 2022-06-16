//SPDX-License-Identifier: MIT
pragma solidity 0.6.0;

contract SimpleStorage {
    uint256 private favoriteNumber;

    struct People {
        string name;
        uint256 favoriteNumber;
    }

    People[] public people;
    mapping(string => People) public nameToNumber;

    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People({name: _name, favoriteNumber: _favoriteNumber}));
        nameToNumber[_name] = people[0];
    }

    function giveValue(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }

    function calculateValue(uint256 _value) public {
        favoriteNumber = favoriteNumber + _value;
    }

    function showValue() public view returns (uint256) {
        return favoriteNumber;
    }
}
