#****************************************************************************
#* vsc_data_model_cpp_gen.py
#*
#* Copyright 2022 Matthew Ballance and Contributors
#*
#* Licensed under the Apache License, Version 2.0 (the "License"); you may 
#* not use this file except in compliance with the License.  
#* You may obtain a copy of the License at:
#*
#*   http://www.apache.org/licenses/LICENSE-2.0
#*
#* Unless required by applicable law or agreed to in writing, software 
#* distributed under the License is distributed on an "AS IS" BASIS, 
#* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
#* See the License for the specific language governing permissions and 
#* limitations under the License.
#*
#* Created on:
#*     Author: 
#*
#****************************************************************************
import io
from vsc_dataclasses.impl.pyctxt.data_type_int import DataTypeInt
from vsc_dataclasses.impl.pyctxt.data_type_struct import DataTypeStruct
from vsc_dataclasses.impl.pyctxt.type_constraint_block import TypeConstraintBlock
from vsc_dataclasses.impl.pyctxt.type_constraint_expr import TypeConstraintExpr
from vsc_dataclasses.impl.pyctxt.type_expr_bin import TypeExprBin
from vsc_dataclasses.impl.pyctxt.type_expr_field_ref import TypeExprFieldRef
from vsc_dataclasses.impl.pyctxt.type_field_phy import TypeFieldPhy
from ..context import BinOp
from ..pyctxt.data_type_struct import DataTypeStruct
from ..pyctxt.visitor_base import VisitorBase

class VscDataModelCppGen(VisitorBase):

    def __init__(self):
        self._ind = ""
        self._out = io.StringIO()
        self._type_s = []

    def generate(self, cls : DataTypeStruct):
        self._out = io.StringIO()
        cls.accept(self)
        return self._out.getvalue()
        pass

    def visitDataTypeInt(self, i: DataTypeInt):
        if (i._is_signed):
            if i._width == 1:
                self.write("bit signed")
            else:
                self.write("bit[%d:0] signed" % (i._width-1))
        else:
            if i._width == 1:
                self.write("bit")
            else:
                self.write("bit[%d:0]" % (i._width-1))

    def visitTypeConstraintBlock(self, i: TypeConstraintBlock):
        self.println("constraint %s {" % i.name())
        self.inc_indent()
        super().visitTypeConstraintBlock(i)
        self.dec_indent()
        self.println("}")

    def visitTypeConstraintExpr(self, i: TypeConstraintExpr):
        self.write(self._ind)
        super().visitTypeConstraintExpr(i)
        self.write(";\n")

    def visitTypeExprBin(self, i: TypeExprBin):
        op_m = {
            BinOp.Eq : "==",
            BinOp.Ne : "!=",
            BinOp.Gt : ">",
            BinOp.Ge : ">=",
            BinOp.Lt : "<",
            BinOp.Le : "<=",
            BinOp.Add : "+",
            BinOp.Sub : "-",
            BinOp.Div : "/",
            BinOp.Mul : "*",
            BinOp.Mod : "%",
            BinOp.BinAnd : "&",
            BinOp.BinOr  : "|",
            BinOp.LogAnd : "&&",
            BinOp.LogOr  : "||",
            BinOp.Sll    : "<<",
            BinOp.Srl    : ">>",
            BinOp.Xor    : "^",
            BinOp.Not    : "~"
        }

        i._lhs.accept(self)
        self.write(" %s " % op_m[i._op])
        i._rhs.accept(self)

    def visitTypeExprFieldRef(self, i: TypeExprFieldRef):
        # TODO: assume in type context
        t = self._type_s[-1]

        for ii in i.getPath():
            f = t.getField(ii)
            self.write("%s" % f.name())

        return super().visitTypeExprFieldRef(i)
    
    def visitTypeFieldPhy(self, i: TypeFieldPhy):
        self.write("%srand " % self._ind)
        i.getDataType().accept(self)
        self.write(" %s;\n" % i.name())
    
    def visitDataTypeStruct(self, i: DataTypeStruct):
        self._type_s.append(i)

        self.println("class %s;" % self.leaf_name(i.name()))
        self.inc_indent()
        super().visitDataTypeStruct(i)
        self.dec_indent()
        self.println("endclass")

        self._type_s.pop()
    
    def println(self, data):
        self._out.write(self._ind)
        self._out.write(data)
        self._out.write("\n")

    def write(self, data):
        self._out.write(data)

    def inc_indent(self):
        self._ind += "    "

    def dec_indent(self):
        if len(self._ind) > 4:
            self._ind = self._ind[:-4]
        else:
            self._ind = ""

    def leaf_name(self, name):
        elems = name.split('.')
        return elems[-1]