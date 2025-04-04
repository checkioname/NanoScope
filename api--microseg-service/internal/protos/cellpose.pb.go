// Code generated by protoc-gen-go. DO NOT EDIT.
// versions:
// 	protoc-gen-go v1.36.6
// 	protoc        v6.30.1
// source: internal/protos/cellpose.proto

package __

import (
	protoreflect "google.golang.org/protobuf/reflect/protoreflect"
	protoimpl "google.golang.org/protobuf/runtime/protoimpl"
	reflect "reflect"
	sync "sync"
	unsafe "unsafe"
)

const (
	// Verify that this generated code is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(20 - protoimpl.MinVersion)
	// Verify that runtime/protoimpl is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(protoimpl.MaxVersion - 20)
)

type ImageRequest struct {
	state         protoimpl.MessageState `protogen:"open.v1"`
	ImageData     []byte                 `protobuf:"bytes,1,opt,name=image_data,json=imageData,proto3" json:"image_data,omitempty"`
	unknownFields protoimpl.UnknownFields
	sizeCache     protoimpl.SizeCache
}

func (x *ImageRequest) Reset() {
	*x = ImageRequest{}
	mi := &file_internal_protos_cellpose_proto_msgTypes[0]
	ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
	ms.StoreMessageInfo(mi)
}

func (x *ImageRequest) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*ImageRequest) ProtoMessage() {}

func (x *ImageRequest) ProtoReflect() protoreflect.Message {
	mi := &file_internal_protos_cellpose_proto_msgTypes[0]
	if x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use ImageRequest.ProtoReflect.Descriptor instead.
func (*ImageRequest) Descriptor() ([]byte, []int) {
	return file_internal_protos_cellpose_proto_rawDescGZIP(), []int{0}
}

func (x *ImageRequest) GetImageData() []byte {
	if x != nil {
		return x.ImageData
	}
	return nil
}

type ImageResponse struct {
	state         protoimpl.MessageState `protogen:"open.v1"`
	Masks         []int32                `protobuf:"varint,1,rep,packed,name=masks,proto3" json:"masks,omitempty"`
	Diams         []float32              `protobuf:"fixed32,2,rep,packed,name=diams,proto3" json:"diams,omitempty"`
	Styles        []float32              `protobuf:"fixed32,3,rep,packed,name=styles,proto3" json:"styles,omitempty"`
	Rows          []float32              `protobuf:"fixed32,4,rep,packed,name=rows,proto3" json:"rows,omitempty"`
	unknownFields protoimpl.UnknownFields
	sizeCache     protoimpl.SizeCache
}

func (x *ImageResponse) Reset() {
	*x = ImageResponse{}
	mi := &file_internal_protos_cellpose_proto_msgTypes[1]
	ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
	ms.StoreMessageInfo(mi)
}

func (x *ImageResponse) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*ImageResponse) ProtoMessage() {}

func (x *ImageResponse) ProtoReflect() protoreflect.Message {
	mi := &file_internal_protos_cellpose_proto_msgTypes[1]
	if x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use ImageResponse.ProtoReflect.Descriptor instead.
func (*ImageResponse) Descriptor() ([]byte, []int) {
	return file_internal_protos_cellpose_proto_rawDescGZIP(), []int{1}
}

func (x *ImageResponse) GetMasks() []int32 {
	if x != nil {
		return x.Masks
	}
	return nil
}

func (x *ImageResponse) GetDiams() []float32 {
	if x != nil {
		return x.Diams
	}
	return nil
}

func (x *ImageResponse) GetStyles() []float32 {
	if x != nil {
		return x.Styles
	}
	return nil
}

func (x *ImageResponse) GetRows() []float32 {
	if x != nil {
		return x.Rows
	}
	return nil
}

var File_internal_protos_cellpose_proto protoreflect.FileDescriptor

const file_internal_protos_cellpose_proto_rawDesc = "" +
	"\n" +
	"\x1einternal/protos/cellpose.proto\x12\bcellpose\"-\n" +
	"\fImageRequest\x12\x1d\n" +
	"\n" +
	"image_data\x18\x01 \x01(\fR\timageData\"g\n" +
	"\rImageResponse\x12\x14\n" +
	"\x05masks\x18\x01 \x03(\x05R\x05masks\x12\x14\n" +
	"\x05diams\x18\x02 \x03(\x02R\x05diams\x12\x16\n" +
	"\x06styles\x18\x03 \x03(\x02R\x06styles\x12\x12\n" +
	"\x04rows\x18\x04 \x03(\x02R\x04rows2R\n" +
	"\x0fCellposeService\x12?\n" +
	"\fProcessImage\x12\x16.cellpose.ImageRequest\x1a\x17.cellpose.ImageResponseB\x03Z\x01/b\x06proto3"

var (
	file_internal_protos_cellpose_proto_rawDescOnce sync.Once
	file_internal_protos_cellpose_proto_rawDescData []byte
)

func file_internal_protos_cellpose_proto_rawDescGZIP() []byte {
	file_internal_protos_cellpose_proto_rawDescOnce.Do(func() {
		file_internal_protos_cellpose_proto_rawDescData = protoimpl.X.CompressGZIP(unsafe.Slice(unsafe.StringData(file_internal_protos_cellpose_proto_rawDesc), len(file_internal_protos_cellpose_proto_rawDesc)))
	})
	return file_internal_protos_cellpose_proto_rawDescData
}

var file_internal_protos_cellpose_proto_msgTypes = make([]protoimpl.MessageInfo, 2)
var file_internal_protos_cellpose_proto_goTypes = []any{
	(*ImageRequest)(nil),  // 0: cellpose.ImageRequest
	(*ImageResponse)(nil), // 1: cellpose.ImageResponse
}
var file_internal_protos_cellpose_proto_depIdxs = []int32{
	0, // 0: cellpose.CellposeService.ProcessImage:input_type -> cellpose.ImageRequest
	1, // 1: cellpose.CellposeService.ProcessImage:output_type -> cellpose.ImageResponse
	1, // [1:2] is the sub-list for method output_type
	0, // [0:1] is the sub-list for method input_type
	0, // [0:0] is the sub-list for extension type_name
	0, // [0:0] is the sub-list for extension extendee
	0, // [0:0] is the sub-list for field type_name
}

func init() { file_internal_protos_cellpose_proto_init() }
func file_internal_protos_cellpose_proto_init() {
	if File_internal_protos_cellpose_proto != nil {
		return
	}
	type x struct{}
	out := protoimpl.TypeBuilder{
		File: protoimpl.DescBuilder{
			GoPackagePath: reflect.TypeOf(x{}).PkgPath(),
			RawDescriptor: unsafe.Slice(unsafe.StringData(file_internal_protos_cellpose_proto_rawDesc), len(file_internal_protos_cellpose_proto_rawDesc)),
			NumEnums:      0,
			NumMessages:   2,
			NumExtensions: 0,
			NumServices:   1,
		},
		GoTypes:           file_internal_protos_cellpose_proto_goTypes,
		DependencyIndexes: file_internal_protos_cellpose_proto_depIdxs,
		MessageInfos:      file_internal_protos_cellpose_proto_msgTypes,
	}.Build()
	File_internal_protos_cellpose_proto = out.File
	file_internal_protos_cellpose_proto_goTypes = nil
	file_internal_protos_cellpose_proto_depIdxs = nil
}
