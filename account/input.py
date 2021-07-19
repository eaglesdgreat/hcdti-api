class Input:

    """New Customer Loan Input field"""

    def newLoanInput(self, request):
        app_type = request.data.get('appType')
        formNo = request.data.get('formNo')
        state = request.data.get('state')
        fullname = request.data.get('fullname')
        nameOfFather = request.data.get('nameOfFather')
        phoneNo = request.data.get('phoneNo')
        residenceAddress = request.data.get('residenceAddress')
        permanentAddress = request.data.get('permanentAddress')
        maritalStatus = request.data.get('maritalStatus')
        formalEdu = request.data.get('formalEdu')
        nextOfKin = request.data.get('nextOfKin')
        phoneNextOfKin = request.data.get('phoneNextOfKin')
        groupOfApp = request.data.get('groupOfApp')
        dateOfMembership = request.data.get('dateOfMembership')
        typeOfBusiness = request.data.get('typeOfBusiness')
        businessDuration = request.data.get('businessDuration')
        busnessAddress = request.data.get('busnessAddress')
        familyOnHcdtiGroup = request.data.get('familyOnHcdtiGroup')
        amtSavingsInPassbook = request.data.get('amtSavingsInPassbook')
        bank = request.data.get('bank')
        accountNo = request.data.get('accountNo')
        lastLoanRecieved = request.data.get('lastLoanRecieved')
        dateLastLoanRepaid = request.data.get('dateLastLoanRepaid')
        loanAppliedFor = request.data.get('loanAppliedFor')
        indeptedToMfbMfi = request.data.get('indeptedToMfbMfi')
        outsanding = request.data.get('outsanding')
        nameOfGuarantor = request.data.get('nameOfGuarantor')
        guarantorRelationship = request.data.get('guarantorRelationship')
        guarantorOccupation = request.data.get('guarantorOccupation')
        guarantorHomeAddress = request.data.get('guarantorHomeAddress')
        guarantorOfficeAddress = request.data.get('guarantorOfficeAddress')
        recFromGroup1 = request.data.get('recFromGroup1')
        recFromGroup2 = request.data.get('recFromGroup2')

        data = {
            "app_type": app_type,
            "formNo": formNo,
            "state": state,
            "fullname": fullname,
            "phoneNo": phoneNo,
            "residenceAddress": residenceAddress,
            "permanentAddress": permanentAddress,
            "maritalStatus": maritalStatus,
            "formalEdu": formalEdu,
            "nextOfKin": nextOfKin,
            "phoneNextOfKin": phoneNextOfKin,
            "groupOfApp": groupOfApp,
            "dateOfMembership": dateOfMembership,
            "typeOfBusiness": typeOfBusiness,
            "businessDuration": businessDuration,
            "busnessAddress": busnessAddress,
            "familyOnHcdtiGroup": familyOnHcdtiGroup,
            "amtSavingsInPassbook": amtSavingsInPassbook,
            "bank": bank,
            "accountNo": accountNo,
            "nameOfFather": nameOfFather,
            "lastLoanRecieved": lastLoanRecieved,
            "dateLastLoanRepaid": dateLastLoanRepaid,
            "loanAppliedFor": loanAppliedFor,
            "indeptedToMfbMfi": indeptedToMfbMfi,
            "outsanding": outsanding,
            "nameOfGuarantor": nameOfGuarantor,
            "guarantorRelationship": guarantorRelationship,
            "guarantorOccupation": guarantorOccupation,
            "guarantorHomeAddress": guarantorHomeAddress,
            "guarantorOfficeAddress": guarantorOfficeAddress,
            "recFromGroup1": recFromGroup1,
            "recFromGroup2": recFromGroup2
        }
        return data

    """Get Existing customer Loan Application Input"""

    def oldLoanInput(self, request):
        app_type = request.data.get('appType')
        formNo = request.data.get('formNo')
        state = request.data.get('state')
        memberNo = request.data.get('memberNo')
        branch = request.data.get('branch')
        lastLoanRecieved = request.data.get('lastLoanRecieved')
        dateLastLoanRepaid = request.data.get('dateLastLoanRepaid')
        loanAppliedFor = request.data.get('loanAppliedFor')
        indeptedToMfbMfi = request.data.get('indeptedToMfbMfi')
        outsanding = request.data.get('outsanding')
        nameOfGuarantor = request.data.get('nameOfGuarantor')
        guarantorRelationship = request.data.get('guarantorRelationship')
        guarantorOccupation = request.data.get('guarantorOccupation')
        guarantorHomeAddress = request.data.get('guarantorHomeAddress')
        guarantorOfficeAddress = request.data.get('guarantorOfficeAddress')
        recFromGroup1 = request.data.get('recFromGroup1')
        recFromGroup2 = request.data.get('recFromGroup2')

        data = {
            "app_type": app_type,
            "formNo": formNo,
            "state": state,
            "memberNo": memberNo,
            "branch": branch,
            "lastLoanRecieved": lastLoanRecieved,
            "dateLastLoanRepaid": dateLastLoanRepaid,
            "loanAppliedFor": loanAppliedFor,
            "indeptedToMfbMfi": indeptedToMfbMfi,
            "outsanding": outsanding,
            "nameOfGuarantor": nameOfGuarantor,
            "guarantorRelationship": guarantorRelationship,
            "guarantorOccupation": guarantorOccupation,
            "guarantorHomeAddress": guarantorHomeAddress,
            "guarantorOfficeAddress": guarantorOfficeAddress,
            "recFromGroup1": recFromGroup1,
            "recFromGroup2": recFromGroup2
        }
        return data
