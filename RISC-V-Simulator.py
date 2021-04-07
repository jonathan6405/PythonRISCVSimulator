#RISC-V (RV32I) Instruction Set Simulator
f=open("tasks/t11.bin","rb") #Loading the file. File location is specified here!
Prog=f.read() #Stores entire program in memory so we don't have to read from disk constantly
pc = 0 #Program Counter
Cycle = 0 #Cycle Counter
Memory=bytearray(1000000000) #Setting the memory
UsedMemory=[] #List that keeps track of memory that has been used
x=list([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
def rshift(val, n): return val>>n if val >= 0 else (val+0x100000000)>>n
#^Defining logical right binary shift
while True:
    Instruction=int.from_bytes(Prog[pc:(pc+4)],byteorder="little")
    #print(str("\n")+bin(Instruction).replace("0b",""))
    opcode = Instruction & 0x7f    
    
    
    if opcode==int("0110111",2):
        rd = (Instruction >> 7) & 0x01f
        imm = (Instruction >> 12)
        print("LUI "+"x"+str(rd)+" "+str(imm))
        bruh=str(bin(imm).replace("0b",""))+"000000000000"  #Adding 12 bits to the immediate
        LUI12=(int(bruh,2)).to_bytes(4, byteorder='big')
        x[rd]=int.from_bytes(LUI12,byteorder="big",signed=False)
        print("Value with added 12 bits is "+str(x[rd]))
    
        
    
    
    elif opcode==int("0010111",2):
        rd = (Instruction >> 7) & 0x01f
        imm = (Instruction >> 12)
        bruh=str(bin(imm).replace("0b",""))+"000000000000" #Adding 12 bits to the immediate
        LUI12=(int(bruh,2)).to_bytes(4, byteorder='big')
        Value=int.from_bytes(LUI12,byteorder="big",signed=False)
        Total=Value+pc
        x[rd]=Total
        print("AUIPC "+"x"+str(rd)+" "+str(imm))
        print("Value with added 12 bits is "+str(Value))
        print("Current PC is "+str(pc))
        print("PC plus offset is "+str(Total))
        
    
    
    elif opcode==int("1101111",2):
        rd = (Instruction >> 7) & 0x01f
        imm19L12 = (Instruction >> 12) & 0xFF   #Splits the immediate up in the appropriate parts
        imm11 = (Instruction >> 20) & 0x1
        imm10L1 = (Instruction >> 21) & 0x3FF
        imm20 = (Instruction >> 31) & 0x1
        bruh=bin(imm10L1).replace("0b","") #Convert the number to binary and adds zero if needed
        Append=10-len(bruh)
        NumberUnsignedPart1=Append*"0"+bruh
        
        bruh=bin(imm11).replace("0b","")
        Append=1-len(bruh)
        NumberUnsignedPart2=Append*"0"+bruh
        
        bruh=bin(imm19L12).replace("0b","")
        Append=8-len(bruh)
        NumberUnsignedPart3=Append*"0"+bruh
        
        bruh=bin(imm20).replace("0b","")
        Append=1-len(bruh)
        NumberUnsignedPart4=Append*"0"+bruh
        
        NumberUnsigned=NumberUnsignedPart4+NumberUnsignedPart3+NumberUnsignedPart2+NumberUnsignedPart1 #Stitches the parts together
        NumberSigned=int(NumberUnsigned[1:20],2)-int(NumberUnsigned[0]+19*"0",2) #Converts back to a number python understands
        if NumberSigned < 0: #When negative, the number is always off by one, not really sure why, but anyways here's a fix for that
            NumberSigned=NumberSigned-1
        
        x[rd]=pc+4
        pc=(pc-4)+NumberSigned #Program counter is decreased by 4 here, as we increase the program counter by 4 at the end of each loop, and we want to ignore that
        print("JAL "+"x"+str(rd)+" "+str(NumberSigned))
     
        
     
        
    elif opcode==int("1100111",2):
        rd = (Instruction >> 7) & 0x01f
        funct3 = (Instruction >> 12) & 0x7 
        rs1 = (Instruction >> 15) & 0x01f
        imm = (Instruction >> 20)
        print("JALR Instruction")
        x[rd]=pc+4
        pc=(-4)+x[rs1]+imm
        print("JALR "+"x"+str(rd)+" "+str(imm)+"(x"+str(rs1)+")")
     
        
     
        
    elif opcode==int("1100011",2):
        #print("BEQ Group")
        imm1 = (Instruction >> 7) & 0x01f
        funct3 = (Instruction >> 12) & 0x7 
        rs1 = (Instruction >> 15) & 0x01f
        rs2 = (Instruction >> 20) & 0x01f
        imm2 = (Instruction >> 25)
        bruh=bin(imm2).replace("0b","") #Basically the same process as in the JAL instruction, just not as many parts
        Append=7-len(bruh)
        NumberUnsignedPart1=Append*"0"+bruh
        bruh=bin(imm1).replace("0b","")
        Append=5-len(bruh)
        NumberUnsignedPart2=Append*"0"+bruh
        NumberUnsigned=NumberUnsignedPart1+NumberUnsignedPart2
        NumberSigned=int(NumberUnsigned[1:12],2)-int(NumberUnsigned[0]+11*"0",2)
        if NumberSigned < 0:
            NumberSigned=NumberSigned-1
        
        if funct3==int("000",2):
            print("BEQ x"+str(rs1)+" x"+str(rs2)+" "+str(NumberSigned))
            if x[rs1] == x[rs2]:
                pc=(pc-4)+NumberSigned
            
        if funct3==int("001",2):
            print("BNE x"+str(rs1)+" x"+str(rs2)+" "+str(NumberSigned))
            if x[rs1] != x[rs2]:
                pc=(pc-4)+NumberSigned
        
        if funct3==int("100",2):
            print("BLT x"+str(rs1)+" x"+str(rs2)+" "+str(NumberSigned))
            if x[rs1] < x[rs2]:
                pc=(pc-4)+NumberSigned
        
        if funct3==int("101",2):
            print("BGE x"+str(rs1)+" x"+str(rs2)+" "+str(NumberSigned))
            if x[rs1] >= x[rs2]:
                pc=(pc-4)+NumberSigned
        
        if funct3==int("110",2):
            print("BLTU x"+str(rs1)+" x"+str(rs2)+" "+str(NumberSigned))
            bruh=bin(x[rs1])
            if bruh[0]=="-":
                Unsigned=32*"1"
                NumberUnsigned1=int(Unsigned,2)+x[rs1]
            else:
                NumberUnsigned1=x[rs1]
            bruh=bin(x[rs2])
            if bruh[0]=="-":
                Unsigned=32*"1"
                NumberUnsigned2=int(Unsigned,2)+x[rs2]
            else:
                NumberUnsigned2=x[rs2]
            if NumberUnsigned1 < NumberUnsigned2:
                pc=(pc-4)+NumberSigned
        
        
        if funct3==int("111",2):
            print("BGEU x"+str(rs1)+" x"+str(rs2)+" "+str(NumberSigned))
            bruh=bin(x[rs1])
            if bruh[0]=="-":
                Unsigned=32*"1"
                NumberUnsigned1=int(Unsigned,2)+x[rs1]
            else:
                NumberUnsigned1=x[rs1]
            bruh=bin(x[rs2])
            if bruh[0]=="-":
                Unsigned=32*"1"
                NumberUnsigned2=int(Unsigned,2)+x[rs2]
            else:
                NumberUnsigned2=x[rs2]
            if NumberUnsigned1 > NumberUnsigned2:
                pc=(pc-4)+NumberSigned
    
            
    
    
    elif opcode==int("0000011",2):
        #print("LB Group")
        rd = (Instruction >> 7) & 0x01f
        funct3 = (Instruction >> 12) & 0x7 
        rs1 = (Instruction >> 15) & 0x01f
        imm = (Instruction >> 20)
        bruh=bin(imm).replace("0b","")
        Append=12-len(bruh)
        NumberUnsigned=Append*"0"+bruh
        NumberSigned=int(NumberUnsigned[1:12],2)-int(NumberUnsigned[0]+11*"0",2)
        if NumberSigned < 0:
            NumberSigned=NumberSigned-1
        
        if funct3==int("000",2):
            print("LB x"+str(rd)+" "+str(NumberSigned)+"(x"+str(rs1)+")")
            x[rd]=int.from_bytes(bytes([Memory[NumberSigned+x[rs1]]]),byteorder="little",signed=True)
            #Loads a number from the bytes, converts it back into a byte, and then converts it into an integer again, this time signed
        
        if funct3==int("001",2):
            print("LH x"+str(rd)+" "+str(NumberSigned)+"(x"+str(rs1)+")")
            x[rd]=int.from_bytes(bytes([Memory[NumberSigned+x[rs1]]])+bytes([Memory[NumberSigned+x[rs1]+1]]),byteorder="little",signed=True)
        
        if funct3==int("010",2):
            print("LW x"+str(rd)+" "+str(NumberSigned)+"(x"+str(rs1)+")")
            x[rd]=int.from_bytes(bytes([Memory[NumberSigned+x[rs1]]])+bytes([Memory[NumberSigned+x[rs1]+1]])+bytes([Memory[NumberSigned+x[rs1]+2]])+bytes([Memory[NumberSigned+x[rs1]+3]]),byteorder="little",signed=True)
            #With multiple bytes, they're all loaded as ints, converted to bytes, and then converted back to ints again but signed
        
        if funct3==int("100",2):
            print("LBU x"+str(rd)+" "+str(NumberSigned)+"(x"+str(rs1)+")")
            x[rd]=int.from_bytes(bytes([Memory[NumberSigned+x[rs1]]]),byteorder="little",signed=False)
        
        if funct3==int("101",2):
            print("LHU x"+str(rd)+" "+str(NumberSigned)+"(x"+str(rs1)+")")
            x[rd]=int.from_bytes(bytes([Memory[NumberSigned+x[rs1]]])+bytes([Memory[NumberSigned+x[rs1]+1]]),byteorder="little",signed=False)
          
            
          
            
    elif opcode==int("0100011",2):
        #print("SB Group")
        imm1 = (Instruction >> 7) & 0x01f
        funct3 = (Instruction >> 12) & 0x7 
        rs1 = (Instruction >> 15) & 0x01f
        rs2 = (Instruction >> 20) & 0x01f
        imm2 = (Instruction >> 25)
        bruh=bin(imm2).replace("0b","")
        #print(bruh)
        Append=7-len(bruh)
        NumberUnsignedPart1=Append*"0"+bruh
        bruh=bin(imm1).replace("0b","")
        #print(bruh)
        Append=5-len(bruh)
        NumberUnsignedPart2=Append*"0"+bruh
        NumberUnsigned=NumberUnsignedPart1+NumberUnsignedPart2
        #print(NumberUnsigned)
        NumberSigned=int(NumberUnsigned[1:12],2)-int(NumberUnsigned[0]+11*"0",2)
        
        if funct3==int("000",2):
            print("SB x"+str(rs2)+" "+str(NumberSigned)+"(x"+str(rs1)+")")
            Binary=bin(x[rs2]).replace("0b","") #Basically a bunch of weird code to get binary to somehow work with all of this
            if Binary[0]=="-":
                Unsigned=32*"1"
                Binary=int(Unsigned,2)+x[rs2]
                print(Binary)
                Binary=bin(Binary).replace("0b","")
            length=len(Binary)
            if length < 9:
                Append=8-len(Binary)
                Byte=Append*"0"+Binary
            else:
                Byte=Binary[length-8:length]
            k=int(Byte,2)
            if k >= 127: #Negative numbers were off by one so this stupid fix is used again
                k+=1
            Memory[NumberSigned+x[rs1]] = k
            print("Writing "+str(k)+" to memory "+str(NumberSigned+x[rs1]))
            UsedMemory.extend([NumberSigned+x[rs1]])
        
        if funct3==int("001",2):
            print("SH x"+str(rs2)+" "+str(NumberSigned)+"(x"+str(rs1)+")")
            Binary=bin(x[rs2]).replace("0b","")
            if Binary[0]=="-":
                Unsigned=32*"1"
                Binary=int(Unsigned,2)+x[rs2]
                #print(Binary)
                Binary=bin(Binary).replace("0b","")
            #print(Binary)
            length=len(Binary)
            if length < 17:
                Append=16-len(Binary)
                ByteBIN=Append*"0"+Binary
            else:
                ByteBIN=Binary[length-16:length]
            #print(ByteBIN)
            NumberBit=int(ByteBIN,2)
            if NumberBit > 32767:
                NumberBit+=1
            Bytes=(NumberBit).to_bytes(2, byteorder='little')
            Memory[NumberSigned+x[rs1]] = Bytes[0]
            Memory[NumberSigned+x[rs1]+1] = Bytes[1]
            print("Writing "+str(NumberBit)+" to memory "+str(NumberSigned+x[rs1])+" and "+str(NumberSigned+x[rs1]+1))
            UsedMemory.extend([NumberSigned+x[rs1]])
            UsedMemory.extend([NumberSigned+x[rs1]+1])

        if funct3==int("010",2):
            print("SW x"+str(rs2)+" "+str(NumberSigned)+"(x"+str(rs1)+")")
            Bytes=(x[rs2]).to_bytes(4, byteorder='little',signed=True) #It's a lot easier to store words as you dont have to chop them up into the smaller halfword or byte parts.
            Memory[NumberSigned+x[rs1]] = Bytes[0]
            Memory[NumberSigned+x[rs1]+1] = Bytes[1]
            Memory[NumberSigned+x[rs1]+2] = Bytes[2]
            Memory[NumberSigned+x[rs1]+3] = Bytes[3]
            print("Writing "+str(x[rs2])+" to memory "+str(NumberSigned+x[rs1])+", "+str(NumberSigned+x[rs1]+1)+", "+str(NumberSigned+x[rs1]+2)+" and "+str(NumberSigned+x[rs1]+3))
            UsedMemory.extend([NumberSigned+x[rs1]])
            UsedMemory.extend([NumberSigned+x[rs1]+1])
            UsedMemory.extend([NumberSigned+x[rs1]+2])
            UsedMemory.extend([NumberSigned+x[rs1]+3])
    
    
    
    
    elif opcode==int("0010011",2):
        #print("ADDI Group")
        rd = (Instruction >> 7) & 0x01f
        funct3 = (Instruction >> 12) & 0x7 
        rs1 = (Instruction >> 15) & 0x01f
        imm = (Instruction >> 20)
        bruh=str(bin(imm).replace("0b",""))
        Append=12-len(bruh)
        NumberUnsigned=Append*"0"+bruh
        NumberSigned=int(NumberUnsigned[1:12],2)-int(NumberUnsigned[0]+11*"0",2)
        
        if funct3==int("000",2):
            print("ADDI x"+str(rd)+" x"+str(rs1)+" "+str(NumberSigned))
            x[rd]=x[rs1]+NumberSigned
        
        if funct3==int("010",2):
            print("SLTI x"+str(rd)+" x"+str(rs1)+" "+str(NumberSigned))
            if x[rs1] < NumberSigned:
                x[rd]=1
        
        if funct3==int("011",2):
            print("SLTIU x"+str(rd)+" x"+str(rs1)+" "+str(NumberSigned))
            bruh=bin(x[rs1])
            if bruh[0]=="-":
                Unsigned=32*"1"
                NumberUnsigned=int(Unsigned,2)+x[rs1]
            else:
                NumberUnsigned=x[rs1]
            if NumberUnsigned < imm:
                x[rd]=1
        
        if funct3==int("100",2):
            print("XORI x"+str(rd)+" x"+str(rs1)+" "+str(NumberSigned))
            x[rd]=x[rs1] ^ NumberSigned
        
        if funct3==int("110",2):
            print("ORI x"+str(rd)+" x"+str(rs1)+" "+str(NumberSigned))
            x[rd]=x[rs1] | NumberSigned
        
        if funct3==int("111",2):
            print("ANDI x"+str(rd)+" x"+str(rs1)+" "+str(NumberSigned))
            x[rd]=x[rs1] & NumberSigned
        
        if funct3==int("001",2):
            shamt = (Instruction >> 20) & 0x01f
            imm = (Instruction >> 25)
            print("SLLI x"+str(rd)+" x"+str(rs1)+" "+str(shamt))
            x[rd]=x[rs1] << shamt
        
        if funct3==int("101",2):
            print("SRLI/SRAI Instruction")
            rd = (Instruction >> 7) & 0x01f
            funct3 = (Instruction >> 12) & 0x7 
            rs1 = (Instruction >> 15) & 0x01f
            shamt = (Instruction >> 20) & 0x01f
            funct7 = (Instruction >> 25)
            
            
            if funct7 == int("0100000",2):
                print("SRAI x"+str(rd)+" x"+str(rs1)+" "+str(shamt))
                x[rd]=x[rs1] >> shamt
            
            if funct7 == 0:
                print("SRLI x"+str(rd)+" x"+str(rs1)+" "+str(shamt))
                x[rd]=rshift(x[rs1],shamt) #Python by default does arithemtic right shifting, and so we use the function to do logical shifting instead
    
    
    
    elif opcode==int("0110011",2):
        rd = (Instruction >> 7) & 0x01f
        funct3 = (Instruction >> 12) & 0x7 
        rs1 = (Instruction >> 15) & 0x01f
        rs2 = (Instruction >> 20) & 0x01f
        funct7 = (Instruction >> 25)
                
        if funct3==int("000",2):
            if funct7 == int("0000000",2):
                print("ADD x"+str(rd)+" x"+str(rs1)+" x"+str(rs2))
                x[rd]=x[rs1]+x[rs2]
            if funct7 == int("0100000",2):
                print("SUB x"+str(rd)+" x"+str(rs1)+" x"+str(rs2))
                x[rd]=x[rs1]-x[rs2]
        
        if funct3==int("001",2):
            print("SLL x"+str(rd)+" x"+str(rs1)+" x"+str(rs2))
            x[rd]=x[rs1] << x[rs2]
        
        if funct3==int("010",2):
            print("SLT x"+str(rd)+" x"+str(rs1)+" x"+str(rs2))
            if x[rs1] < x[rs2]:
                x[rd]=1
            else:
                x[rd]=0
        
        if funct3==int("011",2):
            print("SLTU x"+str(rd)+" x"+str(rs1)+" x"+str(rs2))
            bruh=bin(x[rs1])
            if bruh[0]=="-":
                Unsigned=32*"1"
                NumberUnsigned1=int(Unsigned,2)+x[rs1]
            else:
                NumberUnsigned1=x[rs1]
            bruh=bin(x[rs2])
            if bruh[0]=="-":
                Unsigned=32*"1"
                NumberUnsigned2=int(Unsigned,2)+x[rs2]
            else:
                NumberUnsigned2=x[rs2]
            if NumberUnsigned1 < NumberUnsigned2:
                x[rd]=1
            else:
                x[rd]=0
        
        if funct3==int("100",2):
            print("XOR x"+str(rd)+" x"+str(rs1)+" x"+str(rs2))
            x[rd]=x[rs1] ^ x[rs2]
        
        if funct3==int("101",2):
            
            if funct7 == int("0000000",2):
                print("SRL x"+str(rd)+" x"+str(rs1)+" x"+str(rs2))
                x[rd]=rshift(x[rs1],x[rs2])
                
            if funct7 == int("0100000",2):
                print("SRA x"+str(rd)+" x"+str(rs1)+" x"+str(rs2))
                x[rd]=x[rs1] >> x[rs2]
        
        if funct3==int("110",2):
            print("OR x"+str(rd)+" x"+str(rs1)+" x"+str(rs2))
            x[rd]=x[rs1] | x[rs2]
        
        if funct3==int("111",2):
            print("AND x"+str(rd)+" x"+str(rs1)+" x"+str(rs2))
            x[rd]=x[rs1] & x[rs2]
    
    elif opcode==int("1110011",2): #Most of the code below is basically repeated 3 times as it runs for each loop and also on Ecall and when theres no more code
        print("Ecall Instruction, exiting simulator")
        x[0]=0 #Register zero is always zero, just incase an instruction tries to change it
        for i in range(32):
            if x[i] > 2147483647: #For each loop, the registers are "set correctly" so to say. Basically if a value is outside the -2147483647 - 2147483647 range, it will correct it to be within (basically handles overflow)
                k=bin(x[i]).replace("0b","")
                length=len(k)
                if k[length-32] == "1":
                    x[i]=int(k[length-31:length],2) - 2147483648
                else:
                    x[i]=int(k[length-31:length],2)
        for i in range(32): #Converts the register to unsigned and prints it in hex (This is done only when the simulator ends)
            if x[i] < 0:
                k = x[i]+4294967296
            else:
                k = x[i]
            print("x"+str(i)+" = "+str('0x{0:08X}'.format(k)))
        pc+=4
        Cycle+=1
        print("Used memory addresses are "+str(UsedMemory))
        for i in range(len(UsedMemory)): #Prints the memory that was stored to
            Value=int.from_bytes(bytes([Memory[UsedMemory[i]]]),byteorder="little",signed=True)
            if Value < 0: #Converts to unsigned
                k = Value+256
            else:
                k = Value
            print("Memory "+str('0x{0:08X}'.format(UsedMemory[i]))+" = "+str('0x{0:02X}'.format(k))) #Prints the values in hex
        print("Program Counter is "+str(pc))
        print("Cycle is "+str(Cycle))
        print("------------------------------")
        break
    else:
        print("No more code, exiting simulator")
        x[0]=0
        for i in range(32):
            if x[i] > 2147483647:
                k=bin(x[i]).replace("0b","")
                length=len(k)
                if k[length-32] == "1":
                    x[i]=int(k[length-31:length],2) - 2147483648
                else:
                    x[i]=int(k[length-31:length],2)
        for i in range(32):
            if x[i] < 0:
                k = x[i]+4294967296
            else:
                k = x[i]
            print("x"+str(i)+" = "+str('0x{0:08X}'.format(k)))
        pc+=4
        Cycle+=1
        print("Used memory addresses are "+str(UsedMemory))
        for i in range(len(UsedMemory)):
            print("Memory "+str('0x{0:08X}'.format(UsedMemory[i]))+" = "+str(int.from_bytes(bytes([Memory[UsedMemory[i]]]),byteorder="little",signed=True)))
        print("Program Counter is "+str(pc))
        print("Cycle is "+str(Cycle))
        print("------------------------------")
        break
    for i in range(32):
        if x[i] > 2147483647:
            k=bin(x[i]).replace("0b","")
            length=len(k)
            if k[length-32] == "1":
                x[i]=int(k[length-31:length],2) - 2147483648
            else:
                x[i]=int(k[length-31:length],2)
        if x[i] < -2147483648:
            k=bin(x[i]).replace("0b","")
            length=len(k)
            x[i]=2147483648 - int(k[length-31:length],2)
    x[0]=0
    print(x)
    pc+=4
    Cycle+=1
    print("Program Counter is "+str(pc))
    print("Cycle is "+str(Cycle))
    print("------------------------------")