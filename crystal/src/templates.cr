module KadaluContentApis
  class Template
    def initialize(@conn : Connection, @template_name : String)
    end

    def self.create(conn, template_name, template_type, content)
    end

    def self.list
    end

    def update
    end

    def delete
    end

    def get
    end
  end
end
