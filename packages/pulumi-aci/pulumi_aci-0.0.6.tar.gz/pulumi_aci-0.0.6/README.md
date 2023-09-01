# Pulumi ACI Resource Provider

The Pulumi ACI Resource Provider lets you manage [ACI](https://www.cisco.com/go/aci) resources.

## Installing

This package is available for several languages/platforms:

### Node.js (JavaScript/TypeScript)

To use from JavaScript or TypeScript in Node.js, install using either `npm`:

```bash
npm install @netascode/aci
```

or `yarn`:

```bash
yarn add @netascode/aci
```

### Python

To use from Python, install using `pip`:

```bash
pip install pulumi_aci
```

### Go

To use from Go, use `go get` to grab the latest version of the library:

```bash
go get github.com/netascode/pulumi-aci/sdk/go/...
```

### .NET

To use from .NET, install using `dotnet add package`:

```bash
dotnet add package Pulumi.Aci
```

## Example

### Node.js (JavaScript/TypeScript)

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aci from "@netascode/aci";

const tenant = new aci.apic.Rest(
    "TENANT1",
    {
        dn: "uni/tn-TENANT1",
        class_name: "fvTenant",
        content: {
            "name": "TENANT1",
            "descr": "Tenant created by Pulumi"
        }
    });
```
 
### Python

```python
import pulumi_aci as aci

tenant = aci.apic.Rest(
    "TENANT1",
    dn="uni/tn-TENANT1",
    class_name="fvTenant",
    content={
        "name": "TENANT1",
        "descr": "Tenant created by Pulumi",
    },
)
```

### Go

```go
import (
	"fmt"
	aci "github.com/pulumi/pulumi-aci/sdk/go/aci"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi"
)

func main() {
	pulumi.Run(func(ctx *pulumi.Context) error {

		tenant, err := aci.apic.NewRest(ctx, "TENANT1", &aci.apic.RestArgs{
            Dn: pulumi.String("uni/tn-TENANT1"),
            ClassName: pulumi.String("fvTenant"),
            Content: pulumi.StringMap{
                "name": pulumi.String("TENANT1"),
                "descr": pulumi.String("Tenant created by Pulumi"),
            },
		})
		if err != nil {
			return fmt.Errorf("error creating tenant: %v", err)
		}

		return nil
	})
}
```

### .NET

```csharp
using Pulumi;
using Pulumi.Aci;

class AciTenant : Stack
{
    public AciTenant()
    {
        var tenant = new Rest("TENANT1", new RestArgs{
            Dn: "uni/tn-TENANT1",
            ClassName: "fvTenant",
            Content: {
                { "name", "TENANT1" },
                { "descr", "Tenant created by Pulumi" },
            },
        });
    }
}
```

## Configuration

The following configuration points are available for the `aci` provider:

- `aci:url` (environment: `ACI_URL`) - URL of the Cisco APIC web interface
- `aci:username` (environment: `ACI_USERNAME`) - Username for the APIC Account
- `aci:password` - (environment: `ACI_PASSWORD`) - Password for the APIC Account

## Reference

For detailed reference documentation, please visit [the Pulumi registry](https://www.pulumi.com/registry/packages/aci/api-docs/).