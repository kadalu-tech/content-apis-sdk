module KadaluContentApis
  class Share
    property share_id = ""

    def initialize(@conn : Connection, @share_id : Int64)
    end

    def self.create(conn, bucket_name, public : Bool? = nil,
                    password : String? = nil, password_hash : String? = nil,
                    long_url : Bool? = nil, token : String? = nil, token_hash : String? = nil)
    end

    def self.create(conn, bucket_name, object_path, public : Bool? = nil,
                    password : String? = nil, password_hash : String? = nil,
                    long_url : Bool? = nil, token : String? = nil, token_hash : String? = nil)
    end

    def self.list
    end

    def get
    end

    def delete
    end

    def update
    end
  end
end
